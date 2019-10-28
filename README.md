# Terminal HTML Renderer

## Supported Tags
* p*
* --table*--
  * --td--
  * --tr--
* style

*style-able tags

## Supported Styling Properties of Elements (in units of characters)
* height 
* width 
* margin-bottom
* margin-left
* margin-right
* margin-top

## Syntax
### Style tags
Styling syntax follows the following format:
```
<style-able element> {
  <styling property>: [units in number of characters];
}
```

### Element tags
```
<element></element>
```

Invalid tag syntax will raise a SyntaxError.

## How to Use
### Styling tags
Styling tags apply globally.

### Element tags
Currently, tags do not support nesting.
While element tags can technically contain anything, `table` tags will only display properly with properly nested `tr` and `td` tags.

