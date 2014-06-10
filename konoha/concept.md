# How it works

Each page contains data dictionary and a template name.

Pages have versions. When we save page a new version is created. Both pages and versions store data.
Page's data is equal to the data of its latest version.

Pages could be published. This means that one of the versions is selected to be displayed when the page
is requested by user.

Versions could be valid and not valid. Valid version doesn't produce template error when rendered.
Only valid versions could be published.

# Admin

## List of pages

List view displays list of pages formatted as a tree. The columns are:

- Name
- Path
- Published
- Number of versions

## New page

The new page screen must have:

- Page name (text field)
- Page path (text field)
- Page container (text field)
- Data field (yaml editor)
- Template chooser (combo box)
- Content type field
- Version list. For each version there are links to preview and edit and a button to Publish/Unpublish
- The generic Django buttons ("Save and add another", "Save and continue editing", "Save") and two custom buttons
("Save and publish", "Unpublish" - the last one only if the page is published).

