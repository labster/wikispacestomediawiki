import unittest
import wstomwconverter

class OptionsContainer:
    pass

class TestConverter(unittest.TestCase):
    def setUp(self):    
        filepath = "./test.tmp"
        open(filepath, 'w').write('junk')
    
        options = OptionsContainer()
        options.debug=False
        options.usemedia=False
        options.filelocation="http://localhost/files/"
        
        self.converter = wstomwconverter.WikispacesToMediawikiConverter(filepath, 
                        options)
    
    def test_bold_simple(self):
        self.source_wikitext = \
"""
A paragraph with **some bold text** in it.

Some **multiline 
bold text**
"""
        self.target_wikitext = \
"""
A paragraph with '''some bold text''' in it.

Some '''multiline 
bold text'''
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

    def test_bold_lists(self):
        self.source_wikitext = \
"""
* level 1 list item **some bold text**
** level 2 list item **some bold text**
*** level 3 list item **some bold text**
**** level 4 list item **some bold text** **more bold text**
"""
        self.target_wikitext = \
"""
* level 1 list item '''some bold text'''
** level 2 list item '''some bold text'''
*** level 3 list item '''some bold text'''
**** level 4 list item '''some bold text''' '''more bold text'''
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

    def test_bold_tricky(self):
        self.source_wikitext = \
"""
Some tricky stuff: *****
Wikispaces parses this as a bolded nothing with a star following it.
"""
        self.target_wikitext = \
"""
Some tricky stuff: ''''''*
Wikispaces parses this as a bolded nothing with a star following it.
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

    def test_bold_line_start(self):
        self.source_wikitext = \
"""
** Bulleted text has a space
**No space is bold** text
And extra ** are the just asterisks.
"""
        self.target_wikitext = \
"""
** Bulleted text has a space
'''No space is bold''' text
And extra ** are the just asterisks.
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

    def test_italics_simple(self):
        self.source_wikitext = \
"""
A paragraph with //some italicized text// in it.

Some //multiline
italicized// text.
"""
        self.target_wikitext = \
"""
A paragraph with ''some italicized text'' in it.

Some ''multiline
italicized'' text.
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)
        
    def test_italics_withurls(self):
        self.source_wikitext = \
"""
A paragraph with //some italicized text// in it.

A paragraph with a url: http://www.google.com/
"""
        self.target_wikitext = \
"""
A paragraph with ''some italicized text'' in it.

A paragraph with a url: http://www.google.com/
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

    def test_underline(self):
        self.source_wikitext = \
"""
A paragraph with __some underlined text__ in it.

Some __multiline

underlined__ text.
"""
        self.target_wikitext = \
"""
A paragraph with <u>some underlined text</u> in it.

Some <u>multiline

underlined</u> text.
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)
        
    def test_monospaced(self):
        self.source_wikitext = \
"""
A paragraph with {{some monospaced text}} in it.

Some {{multiline

monospaced}} text.
"""
        self.target_wikitext = \
"""
A paragraph with <tt>some monospaced text</tt> in it.

Some <tt>multiline

monospaced</tt> text.
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

    def test_variables(self):
        self.source_wikitext = \
"""
A paragraph with {$page} in it.
"""
        self.target_wikitext = \
"""
A paragraph with test.tmp in it.
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

        
    def test_includes(self):
        self.source_wikitext = \
"""
A paragraph.

[[include page="somepage"]]

[[include page="somepage" title="some title"]]

[[include page="somepage" editable="true"]]

[[include page="somepage" wrap="true"]]
"""
        self.target_wikitext = \
"""
A paragraph.

{{:somepage}}

{{:somepage}}

{{:somepage}}

{{:somepage}}
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

    def test_toc(self):
        self.source_wikitext = \
"""
A paragraph...

[[toc]]

[[toc|flat]]
"""
        self.target_wikitext = \
"""
A paragraph...


"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

    def test_external_links(self):
        self.source_wikitext = \
"""
A paragraph with [[http://example.com|an external link]].

Another paragraph with [[https://example.com|an external link]].

Yet another paragraph with [[ftp://example.com|an external link]].
"""
        self.target_wikitext = \
"""
A paragraph with [http://example.com an external link].

Another paragraph with [https://example.com an external link].

Yet another paragraph with [ftp://example.com an external link].
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

    def test_naked_external_links(self):
        self.source_wikitext = \
"""
A paragraph with a [[http://example.com]] naked external link. Link should 
simply be stripped of brackets.

Another [[ftp://example.com]] naked external link.

And another one [[https://example.com]].

A really naked one here: http://example.com. Nothing should happen to it.
"""
        self.target_wikitext = \
"""
A paragraph with a http://example.com naked external link. Link should 
simply be stripped of brackets.

Another ftp://example.com naked external link.

And another one https://example.com.

A really naked one here: http://example.com. Nothing should happen to it.
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

    def test_file_links(self):
        self.source_wikitext = \
"""
A paragraph with [[file:somefile.doc]].

Another paragraph with [[file:somefile.tex|a tex file]].
"""
        self.target_wikitext = \
"""
A paragraph with [http://localhost/files/somefile.doc somefile.doc].

Another paragraph with [http://localhost/files/somefile.tex a tex file].
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

    def test_file_links_withmedia(self):
        self.source_wikitext = \
"""
A paragraph with [[file:somefile.doc]].

Another paragraph with [[file:somefile.tex|a tex file]].
"""
        self.target_wikitext = \
"""
A paragraph with [[Media:somefile.doc]].

Another paragraph with [[Media:somefile.tex|a tex file]].
"""
        self.converter.content = self.source_wikitext
        self.converter.options.usemedia = True
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

    def test_code_tags(self):
        self.source_wikitext = \
"""
A paragraph with [[code]]some code in it[[code]].

[[code]]
Some
multiline
code
[[code]]

Yet another paragraph with [[code]]some
multiline
code
[[code]]
"""
        self.target_wikitext = \
"""
A paragraph with <pre>some code in it</pre>.

<pre>
Some
multiline
code
</pre>

Yet another paragraph with <pre>some
multiline
code
</pre>
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

    def test_code_tags_verbatim(self):
        self.source_wikitext = \
"""
A paragraph with [[code]]some code **in it**[[code]].

[[code]]
Some
multiline [[http://somestuff.com|morestuff]]
code
[[code]]

Yet another paragraph with [[code]]some
//multiline//
code
[[code]]
"""
        self.target_wikitext = \
"""
A paragraph with <pre>some code **in it**</pre>.

<pre>
Some
multiline [[http://somestuff.com|morestuff]]
code
</pre>

Yet another paragraph with <pre>some
//multiline//
code
</pre>
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

    def test_math_tags(self):
        self.source_wikitext = \
"""
A paragraph with [[math]]some math in it[[math]].

[[math]]
Some
multiline
math
[[math]]

Yet another paragraph with [[math]]some
multiline
math
[[math]]
"""
        self.target_wikitext = \
"""
A paragraph with <math>some math in it</math>.

<math>
Some
multiline
math
</math>

Yet another paragraph with <math>some
multiline
math
</math>
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

    def test_image_tags(self):
        self.source_wikitext = \
"""
A paragraph with an image:
[[image:somefile.gif width="20" height="80" align="left" link="http://example.com" caption="some caption"]].

A paragraph with a simpler image: [[image:somefile.gif]]

A paragraph with a medium-complexity image: [[image:somefile.gif height="80" align="right"]]

An image that should become a thumb:
[[image:somefile.gif width="20" height="80" align="left" caption="some caption"]]
"""
        self.target_wikitext = \
"""
A paragraph with an image:
[[File:somefile.gif|20x80px|left|link=http://example.com|some caption]].

A paragraph with a simpler image: [[File:somefile.gif]]

A paragraph with a medium-complexity image: [[File:somefile.gif|x80px|right]]

An image that should become a thumb:
[[File:somefile.gif|thumb|20x80px|left|some caption]]
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

    def test_indents(self):
        self.source_wikitext = \
"""
A paragraph with some <stuff>

> an indented paragraph

>> an even more indented paragraph with some > stuff.
"""
        self.target_wikitext = \
"""
A paragraph with some <stuff>

: an indented paragraph

:: an even more indented paragraph with some > stuff.
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)
        
    def test_tables_simple(self):
        self.source_wikitext = \
"""
A paragraph...

|| A simple || table ||
|| with two || rows ||

|| a table || with a

multiline cell ||
|| and another
multiline cell || and a cell ||
"""
        self.target_wikitext = \
"""
A paragraph...

{| style="border: 1px solid #c6c9ff; border-collapse: collapse;" cellspacing="0" cellpadding="10" border="1"
|-
| A simple 
| table 
|-
| with two 
| rows 
|}

{| style="border: 1px solid #c6c9ff; border-collapse: collapse;" cellspacing="0" cellpadding="10" border="1"
|-
| a table 
| with a

multiline cell 
|-
| and another
multiline cell 
| and a cell 
|}
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

    def test_tables_fancy(self):
        self.source_wikitext = \
"""
A paragraph...

||~ heading1 ||~ heading2 ||
||= aligned center ||> aligned right ||

||~ a table ||~ with a

multiline cell ||
||> and another
multiline cell ||= and a cell ||
"""
        self.target_wikitext = \
"""
A paragraph...

{| style="border: 1px solid #c6c9ff; border-collapse: collapse;" cellspacing="0" cellpadding="10" border="1"
|-
! heading1 
! heading2 
|-
|align="center" | aligned center 
|align="right" | aligned right 
|}

{| style="border: 1px solid #c6c9ff; border-collapse: collapse;" cellspacing="0" cellpadding="10" border="1"
|-
! a table 
! with a

multiline cell 
|-
|align="right" | and another
multiline cell 
|align="center" | and a cell 
|}
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

    def test_escapes(self):
        self.source_wikitext = \
"""
A paragraph with some ``escaped stuff``.

A paragraph with some ``escaped stuff that would **otherwise be parsed**``.
"""
        self.target_wikitext = \
"""
A paragraph with some <nowiki>escaped stuff</nowiki>.

A paragraph with some <nowiki>escaped stuff that would **otherwise be parsed**</nowiki>.
"""
        self.converter.content = self.source_wikitext
        self.converter.run_regexps()
        self.assertEqual(self.converter.content, self.target_wikitext)

if __name__ == '__main__':
    unittest.main()
