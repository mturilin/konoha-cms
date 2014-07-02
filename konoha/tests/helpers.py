from urlparse import urlsplit, urlunsplit

from django.http import QueryDict


__author__ = 'mikhailturilin'


def response_template_names(response):
    return [t.name for t in response.templates]


def assert_redirects_to(response, expected_url, status_code=302,
                        target_status_code=200, host=None, msg_prefix=''):
    if hasattr(response, 'redirect_chain'):
        # The request was a followed redirect
        assert len(response.redirect_chain) > 0, "Response didn't redirect as expected: Response" \
                                                 " code was %d (expected %d)" % (response.status_code,
                                                                                 status_code)

        assert response.redirect_chain[0][1] == status_code, \
            "Initial response didn't redirect as expected:Response code was %d (expected %d)" % \
            (response.redirect_chain[0][1], status_code)

        url, status_code = response.redirect_chain[-1]

        assert response.status_code == target_status_code, \
            "Response didn't redirect as expected: Final" \
            " Response code was %d (expected %d)" % \
            (response.status_code, target_status_code)

    else:
        # Not a followed redirect
        assert response.status_code == status_code, "Response didn't redirect as expected: Response" \
                                                    " code was %d (expected %d)" % \
                                                    (response.status_code, status_code)

        url = response.url
        scheme, netloc, path, query, fragment = urlsplit(url)

        redirect_response = response.client.get(path, QueryDict(query))

        # Get the redirection page, using the same client that was used
        # to obtain the original response.
        assert redirect_response.status_code == target_status_code, \
            "Couldn't retrieve redirection page '%s': response code was %d (expected %d)" % \
            (path, redirect_response.status_code, target_status_code)

    e_scheme, e_netloc, e_path, e_query, e_fragment = urlsplit(expected_url)

    if not (e_scheme or e_netloc):
        expected_url = urlunsplit(('http', host or 'testserver', e_path, e_query, e_fragment))

    assert url == expected_url, "Response redirected to '%s', expected '%s'" % (url, expected_url)