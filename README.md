# Changelog Manager

This is a simple tool for parsing and manipulating changelog's formatted according to the [Keep a Changelog](https://keepachangelog.com/) standard.

It uses [Mistune](https://github.com/lepture/mistune) to parse the Markdown text and the [lxml](https://github.com/lxml/lxml) ElementTree API to traverse, manipulate and serialize the changelog.

## Changelog format

The following rules apply to the changelog format:

- The file must start with a level 1 heading with the title of the changelog
- Immediately following the level 1 heading there must be one or more paragraphs describing the content (an introduction)
- There should be one level 2 heading per released version and one containing upcoming changes
- Each level 2 heading should contain one or more level 3 headings whose title is one of the allowed types of changes
- Each level 3 heading should contain a list with one or more items describring particular changes
