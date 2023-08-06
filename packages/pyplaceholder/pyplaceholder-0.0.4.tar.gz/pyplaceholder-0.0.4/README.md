# pyplaceholder
A placeholder detector in text or in text files and other placeholder utilities. 
A placeholder is a piece of text delimited by some symbols

* [Detect the placeholders](#detect-the-placeholders)
* [Replace text placeholders](#replace-text-placeholders)
* [Check if there are placeholders](#check-if-there-are-placeholders)
* [Count placeholders](#count-placeholders)
* [Get the placeholder contents](#get_placeholder_contents)

# Detect the placeholders<a id="detect-the-placeholders" name="detect-the-placeholders"></a>

To detect the placeholder positions of a given text you can use the parse_placeholders() function:

```python
def parse_placeholders(text: str,
                       open_ch: str = '{',
                       close_ch: str = '}',
                       escapes: bool = True) -> Tuple[str, List[Tuple[int, int]]]:
```

Where _text_ is the text with placeholders to detect;
_open_ch_ is the initial symbol of the placeholder and _close_ch_ is the final one;
_escapes_ if True if you want that the escaped character '\' should be escaped in the final returned text.
This function returns a tuple with the parsed text without escape characters,
and a list of positions with the initial and end position of each placeholder in that text.

For example, if you have a text like the following: 

```python
s = 'Some example of {term} \\{UN\\}'
```

If you want to detect the {terms} but not {UN} because it is escaped with \\, then you need to execute:

```python
from placeholder import parse_placeholders
s = 'Some example of {term} \\{UN\\}'
parse_placeholders(s)
```

Therefore, it will return the following results:

```python
('Some example of {term} {UN}', [(16, 22)])
```

Where, here, the placeholder is {terms}. The placeholder has to be delimited by just one character, but not more.
The placeholder delimiters can be changed by using the parameters **open_ch** and **close_ch**:

```python
from placeholder import parse_placeholders
s = 'Some example of <term> {UN}'
parse_placeholders(s, '<', '>')
```

The result will be similar, and now we do not need to escape the characters {} for {UN} because we have changed the
default delimiters:


```python
('Some example of <term> {UN}', [(16, 22)])
```

In this case the placeholder is &lt;term&gt;.

Finally, you can detect the placeholders from a text without parse the escape characters changing the parameter 
**escapes**.

If there are more than one placeholders, the results will be a list of positions.
For example:

```python
from placeholder import parse_placeholders
s = 'Some example of {term} {UN}'
parse_placeholders(s)
```

The output will be:

```python
('Some example of {term} {UN}', [(16, 22), (23, 27)])
```

In this case, it detects both placeholders because the second one was not escaped with \\.

# Replace text placeholders<a id="replace-text-placeholders" name="replace-text-placeholders"></a>
With this module you can replace the placeholders using **replace_placeholders()** or **replace_file_placeholders()**.
The first one is to work with a string value and the second one to replace in a text file.

The syntax of the **replace_placeholders()** function is:

```python
def replace_placeholders(text: str,
                         open_ch: str = '{',
                         close_ch: str = '}',
                         escapes: bool = True,
                         **kwargs) -> str:
```

Where _text_ is the text with placeholders to detect;
_open_ch_ is the initial symbol of the placeholder and _close_ch_ is the final one;
_escapes_ if True if you want that the escaped character '\' should be escaped in the final returned text;
and, finally, _kwargs_ are the value of the text placeholders. 
The result of executing this functions will be the same string as the input but with the placeholders 
replaced by they related values.
For example:


```python
from placeholder import replace_placeholders
s = 'Some example of {term} \\{UN\\}'
print(replace_placeholders(s, term='United Nations'))
```

It will replace the placeholder '{term}' by the text "United Nations".
Therefore, the result will be:

```text
Some example of United Nations {UN}
```

The syntax of **replace_file_placeholders()** is very similar:

```python
def replace_file_placeholders(input_file: Union[str, PathLike, bytes],
                              output_file: [str, PathLike, bytes],
                              open_ch: str = '{',
                              close_ch: str = '}',
                              escapes: bool = True,
                              **kwargs) -> None:
```

However, this function uses an input and output files instead a string. 
For example, if we have the following test.txt file:

```text
This is a test with {num} placeholders to {action} the functions to parse \{placeholders\}.
Other line without placeholders.
```

And we execute the following:

```python
from placeholder import replace_file_placeholders

replace_file_placeholders('test.txt', 'test2.txt', num=2, action='test')
```

This will generate a output file 'test2.txt' with the following content:

```text
This is a test with 2 placeholders to test the functions to parse {placeholders}.
Other line without placeholders.
```

# Check if there are placeholders<a id="check-if-there-are-placeholders" name="check-if-there-are-placeholders"></a>
It is possible to use **has_placeholders()** function to check if a text has placeholders or not:

```python
def has_placeholders(text: str, open_ch: str = '{', close_ch: str = '}') -> bool:
```

Where _text_ is the text with placeholders to detect;
_open_ch_ is the initial symbol of the placeholder and _close_ch_ is the final one.
This function returns True if there is any placeholder delimited by those characters.
For example:

```python
from placeholder import has_placeholders
s = 'Some example of {term} \\{UN\\}'
has_placeholders(s)  # Return True
s = 'Some example of {term} {UN}'
has_placeholders(s)  # Return True
s = 'Some example of \\{term\\} \\{UN\\}'
has_placeholders(s)  # Return False
s = 'Some example of term UN'
has_placeholders(s)  # Return False
```

# Count placeholders<a id="count-placeholders" name="count-placeholders"></a>
Count the number of placeholders of a string.

```python
def num_placeholders(text: str, open_ch: str = '{', close_ch: str = '}') -> int: 
```

Where _text_ is the text with placeholders to detect;
_open_ch_ is the initial symbol of the placeholder and _close_ch_ is the final one.
This function will return the number of detected placeholders delimited by those characters.
For example:

```python
from placeholder import num_placeholders

s = 'Some example of {term} \\{UN\\}'
num_placeholders(s)  # Returns 1
s = 'Some example of {term} {UN}'
num_placeholders(s)  # Returns 2
s = 'Some example of \\{term\\} \\{UN\\}'
num_placeholders(s)  # Returns 0
s = 'Some example of term UN'
num_placeholders(s)  # Returns 0
```

# Get the placeholder contents<a id="get_placeholder_contents" name="get_placeholder_contents"></a>
We have two functions to get the placeholder content: 
**get_placeholders()**, **get_placeholder()**, **get_file_placeholders()**, **get_file_placeholder()**.
The first one obtains a list with all the placeholder values in the input string.
The second one get only one specific placeholder.
The other two functions are the equivalent ones but using a file text instead a string as input. 

The definition of the first is:

```python
def get_placeholders(text: str,
                     open_ch: str = '{',
                     close_ch: str = '}',
                     type: Union[Callable, List[Callable]] = str) -> List[Any]:
```

Where _text_ is the text with placeholders to detect;
_open_ch_ is the initial symbol of the placeholder and _close_ch_ is the final one;
and _type_ is the type or types to convert the placeholder values.
This function returns a list of values with each placeholder value.
For example:

```python
from placeholder import get_placeholders
s = 'Some example of {term} \\{UN\\}'
get_placeholders(s)  # This returns ['term']
s = 'Some example of {term} {UN}'
get_placeholders(s)  # This returns ['term', 'UN']
s = 'Some example of {1} and {2}'
get_placeholders(s)  # This returns ['1', '2']
get_placeholders(s, type=int)  # This returns [1, 2]
s = 'Some example of {1} and {term}'
get_placeholders(s, type=[int, str])  # This rturns [1, 'term']
```

The function **get_placeholder()** is very similar but only returns one placeholder. 
By default, it returns the first one. Its syntax is:

```python
def get_placeholder(text: str,
                    open_ch: str = '{',
                    close_ch: str = '}',
                    type: Callable = str,
                    pos: int = 0) -> Any:
```

Where _type_, in this case, has just one value and _pos_ is the position of the placeholder.
For example:

```python
from placeholder import get_placeholder

s = 'Some example of {term} \\{UN\\}'
get_placeholder(s)  # This returns 'term'
s = 'Some example of {term} {UN}'
get_placeholder(s)  # This returns 'term'
get_placeholder(s, pos=1)  # This returns 'UN'
s = 'Some example of {1} and {2}'
get_placeholder(s)  # This returns '1'
get_placeholder(s, type=int)  # This returns 1
get_placeholder(s, type=int, pos=1)  # This returns 2
```

The function **get_file_placeholders()** and **get_placeholder()** have the following signature:

```python
def get_file_placeholders(file: Union[str, PathLike, bytes],
                          open_ch: str = '{',
                          close_ch: str = '}',
                          type: Callable = str) -> List[Any]:

def get_file_placeholder(file: Union[str, PathLike, bytes],
                         open_ch: str = '{',
                         close_ch: str = '}',
                         type: Callable = str,
                         pos: int = 0) -> Any:
```

With _file_ to the file path instead of the string.
The first one return the list with the content of all the placeholders delimited by those characters, and
the other one returns only one placeholder in that position.
For example, if we have the following test.txt file:

```text
This is a test with {num} placeholders to {action} the functions to parse \{placeholders\}.
Other line without placeholders.
```

We can execute the following:

```python
from placeholder import get_file_placeholders, get_file_placeholder

get_file_placeholders('test.txt')  # Returns ['num', 'action']
get_file_placeholder('test.txt')  # Returns 'num'
get_file_placeholder('test.txt', pos=2)  # Returns 'action'
get_file_placeholder('test.txt', pos=-1)  # Returns 'action'
```