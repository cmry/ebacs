#!/usr/bin/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from collections import OrderedDict as OD
from copy import deepcopy
from re import findall
from json import loads

__author__ = 'chris'
__version__ = '05.15'

bib = {}
retr = []  # add id numbers which have retracted


def sanitize(texs, istex=None):
    """
    Escapes any colliding characters with LaTeX, correct stupid unicode
    characters, and do a clean-up on some other user/system errors.

    :param texs: str abstract (or any) text in unicode
    :return: str sanitized text ready for LaTeX compiling
    """
    cust = {  # custom replacements go here
            'htttp':                                        u'http',
            # LaTeX collides
            '{':                                            u'\{',
            '}':                                            u'\}',
            " ''":                                          u" ``",
            " '":                                           u" `",
            "&":                                            u"\&",
            "~":                                            u"\~",
            "\%":                                           u"%",
            "%":                                            u"\%",  # wtf?
            "_":                                            u"\_",
            # crappy mac unicode stuff
            u'\u00A0':                                      u" ",
            u'\u00AD':                                      u"",
            # system errors
            "&amp;":                                        u"&",
            "amp;":                                         u''
            }

    for orig, repl in cust.iteritems():
        texs = texs.replace(orig, repl)
    if not istex:  # text only
        texs = texs.replace('\n', ' ')
        # texs = token_url(texs, True)
    return texs


def token_url(text, fn=False):
    """
    Recognizes URLs in text and format them so that they will be
    placed in a footnote underneath the abstract. It also makes sure
    that certain stylistic clashes are omitted, for example a colon
    before the footnote number.

    :param text: str unicode text
    :return: str with footnoted URLs
    """
    # TODO: smarter handling of footnote
    urls = findall(' ?(?:(?:http|ftp|https):\/\/[a-z./0-9%]|\/?www).*(?:\.[a-z]{2,5}|\/)(?: |\n|\.|\)|,|$)', text)
    if urls:
        for u in urls:
            lm = u[len(u)-1:]  # try to trim stuff before the URL
            u = u[:-1] if (lm == '.' or lm == ')' or lm == ',') else u  # trim
            text = text.replace(u, ("\\footnote{" if fn else '') + " \\url{"+u+"}" + ("}" if fn else ''))  # insert footnote
    if fn:
        burls = findall('(?:,|\.)' + ('\\\\footnote\{' if fn else '') + ' \\\\url\{.*\}' + ('\}' if fn else ''), text)
        if burls:  # if , or . before footnote, switch them
            for bu in burls:
                text = text.replace(bu, bu[1:]+bu[0])
    return text


def format_ref(refs, label):
    """
    Given a string with references able to be splitted by newline,
    adds to global bib a tuple with a unique id, and the label it
    will use to refer to the page it's mentioned on, as well as a
    cleaned out version of the references. Custom part had to be
    implemented because one of the references was split up by
    newlines within references.

    :param refs: str unicode text snippet with \n splittable refs
    :param label: here sec:title is used to pageref to the abstract
    :return: None (adds to global bib)
    """
    global bib
    refs = refs.split('\n')
    for n in refs:
        if len(n) > 10:
            n = n[1:] if n.startswith(' ') else n
            # n = token_url(n)
            bib[(hash(n), label)] = n


def format_text(text, title):
    """
    Finds the boundary between the list of references and the
    abstract text, will provide a label for the abstract, and
    pipe the found references towards format_ref function.

    :param text: the abstracts text, including refs
    :param title: the title of the abstract
    :return: str unicode with the abstract text and label, no refs
    """
    ref = findall(r'\n(?:[Rr]eference)|(?:REFERENCE)[sS]?[:]?', text)
    brf = findall(r'\n\[[0-9]\]', text)
    label = 'tit:' + str(hash(title))
    if brf or ref:
        tl = text.split((brf[-1:] if (brf and not ref) else ref[-1:])[0])
        text, ref = tl[0], sanitize(tl[1], True)
        format_ref(ref, label)
    return '\\noindent '+sanitize(text)+'\n'+'\\label{'+label+'}'


def format_toc(tit, name_l):
    """
    Accepts title and list of tuples with names from the authors
    of the abstract, and will convert these into a formatted unicode
    LaTeX toc entry.

    :param tit: str unicode abstract title (no linebreaks)
    :param name_l: list str with authors
    :return: str unicode ToC entry for the abstract
    """
    # TODO: refactor this function to look more like the one on fazzeh.github.io
    aut = ', '.join([('\\newline ' if (name_l.index(n) == 4 and len(', '.join([n[0]+' '+n[1] for n in name_l[:3]]))
                                       < 72) else '') + n[0]+' '+n[1] for n in name_l])
    aut = aut.split(' \\newline')
    tit = tit.replace('\\\\ ', '')
    tit = "\\addcontentsline{toc}{section}{\\emph{" + tit + "}} \n" + \
          "\\addtocontents{toc}{\\protect\\vspace{0.2em}} \n" + \
          "\\addtocontents{toc}{" + aut[0] + " \\hfill" + ("\\newline" if len(aut) > 1 else '') + "} \n"
    if len(aut) > 1:
        tit += "\\addtocontents{toc}{\\hspace*{1.2em}" + aut[1] + "} \n"
    tit += "\\addtocontents{toc}{\\protect\\vspace{1em}} \n"
    return tit


def check_prio(tl):
    """
    Checks if there is a character in the title which has priority
    as being a split marker.

    :param tl: str unicode title of the abstract
    :return: int index of the priority if exists, else None
    """
    mark = [':' if ':' in i else False or '(' if '(' in i else False for i in tl]
    if '(' in mark:
        if mark.index('(') > 2:
            return mark.index('(')
    elif ':' in mark:
        if mark.index(':') > 2:
            return mark.index(':')+1


# TODO: check if for each function it is mentioned if they output LaTeX
def format_title(title):
    """
    Will _try_ to make an intelligent decision on where to split
    the inputted title. Please be aware that this is font/point/
    page specific as it will incorporate length. 62 < len(title)
    < 96. Will try to figure out some variables for this.

    :param title: str title without any breaks (yet)
    :return: 'intelligently' splitted title for LaTeX
    """
    # TODO: try to make 62 < x < 96 user handable, check page 41
    newline_indicators = ['and', 'the', 'a', 'for', 'in']
    title = sanitize(title)
    if 62 < len(title) < 96:
        title_list = title.split()
        title_list.insert(len(title_list)/2 if not check_prio(title_list) else check_prio(title_list), '\\\\')
        for word in list(set(title_list) & set(newline_indicators)):
            if title_list.index(word)-title_list.index('\\\\') == 1 and ':' not in title_list[title_list.index(word)-2]:
                a, b = title_list.index(word), title_list.index('\\\\')
                title_list[a], title_list[b] = title_list[b], title_list[a]
        title = ' '.join(title_list)
    if title[-1:] == '.':
        title = title[:-1]
    return title


def lower_dutch_prep(surename):
    """
    Converts 'incorrectly' capitalized Dutch surenames to a more
    conistent format.

    :param surename:
    :return:
    """
    prep_list = {'Van ': 'van ', 'Den ': 'den ', 'Der ': 'der ', 'De ': 'de ',
                 'Het ': 'het ', "'T ": "'t ", 'Des ': 'des ', 'Op ': 'op '}
    for ini in prep_list.iterkeys():
        if ini in surename:
            surename = surename.replace(ini, prep_list[ini])
    return surename


def format_name(name):
    """
    Joins and formats name with index. Might be superflous.

    :param name: tup with (first, last) name.
    :return: str joined name with index reference
    """
    st_name = name[0]+' '+name[1]
    return st_name + " \\index{" + name[1] + ", " + name[0] + "} "


def author_tab(bottom=False):
    """
    Outputs table that is utilized to properly format the list
    of authors, neatly centered, in the abstract.

    :param bottom: bool want the bottom part of the table?
    :return: str part of the author table
    """
    return '''
        \\begin{table}[t!]
        \\makebox[\\textwidth]{
        \\centering
        \\begin{tabular}{---al---}
        ---ta--- ''' if not bottom else '''
        \\end{tabular} }
        \\end{table} '''


def format_table(namel, afil, maill):
    """
    Pretty elaborate function that determines how to format the
    tables used to format the auhtor lists. In this format, it
    is chosen to keep positioning the authors with two in a row,
    until there is only one left, that one will be centered in
    a new table with an allignment of only one {c}.

    :param namel: list with full author names in str format
    :param afil: list with author affiliations in str format
    :param maill: list with contact emails in str format
    :return: one (in case of 1-2 authors) or two (>2) author
             LaTeX tables
    """
    ltab = []
    while len(namel) > 0:
        ntab = deepcopy(author_tab())
        if len(namel) == 1:
            if len(ltab) != 0:
                ntab = author_tab(True) + ntab
            ntab += author_tab(True)
            name_e = format_name(namel.pop(0))
            ta = "%s \\\\ %s \\\\ {\\texttt{%s}} \\\\" % (name_e, afil.pop(0), maill.pop(0))
            al = 'c'
        else:
            name_e1 = format_name(namel.pop(0))
            name_e2 = format_name(namel.pop(0))
            ta = "%s & %s \\\\ {%s} & {%s} \\\\ {\\texttt{%s}} & {\\texttt{%s}} \\\\" % \
                 (name_e1, name_e2, afil.pop(0), afil.pop(0), maill.pop(0), maill.pop(0))
            al = 'cc'
        if al == 'cc' and len(ltab) >= 1:
            ntab = " & \\\\ \n "+ta
        else:
            ntab = ntab.replace('---ta---', ta)
            ntab = ntab.replace('---al---', al)
        ltab.append(ntab)
    if '\\end{table}' not in ltab[len(ltab)-1]:
        ltab.append(author_tab(True))
    return '\n'.join(ltab)


# TODO: make the two tables as in these functions
def agt(a, c):
    """
    Formats the table for the agenda, in landscape, and uses set-
    lenght to center.

    :param a: str the alignments and borders for the table in
              LaTeX format
    :param c: list of str with table lines constructed in
              get_agenda
    :return: str LaTeX table with inserted content
    """
    return '''
    \\begin{landscape}
    \\begin{centering}
    \\begingroup
    \\setlength{\LTleft}{-20cm plus -1fill}
    \\setlength{\LTright}{\LTleft}
    \\footnotesize
    \\begin{longtable}{%s}
    \\toprule
    %s
    \\bottomrule
    \\end{longtable}
    \\endgroup
    \\end{centering}
    \\end{landscape}''' % (a, c)


# TODO: it might a nice idea to store the LaTeX commands in a function to call in python
def get_agenda(d):
    """
    This will construct a conference programme using a dict with
    submissions id, author and titles according to the specified
    ordering in agenda.json. In the newest version, HTML is also
    incorporated which makes it an ugly-ass function, please make
    sure to generalize and split into two seperate output functions,
    using markdown as a base or something.

    :param d: dict with int(id): tup(authors, title)
    :return: str agenda in a LaTeX table
    """
    # TODO: try to generalize this stuff to be LaTeX unspecific
    lin, ltml = list(), list()
    with open('agenda.json', 'r') as f:
        l = loads(f.read())
    for entry in sorted(l["agenda"]):

        event = l["agenda"][entry]
        if "what" in event:  # Plenary
            lin.append('\\midrule \n %s & \\multicolumn{5}{l}{\\textbf{%s:} %s %s in %s} \\\\' % (event["time"], event["name"], event["what"], event["by"], event["room"]))
            ltml.append('<tr><td>%s</td><td colspan="5"><b>%s</b>: %s %s in %s</td></tr> \n' % (event["time"], event["name"], event["what"], event["by"], event["room"]))
        elif "sessions" in event:  # Talks
            namel, rooml, block_m = [], [], []
            for s in event["sessions"]:
                inf = event["sessions"][s]
                namel.append(inf["name"])
                rooml.append(inf["room"])
                block_m.append(inf["blocks"])
            lin.append('\\midrule \n \\textbf{%s} & %s \\\\ \n %s & \\textbf{%s} \\\\' % (event["name"], ' & '.join(rooml), event["time"], '} & \\textbf{'.join(namel)))
            ltml.append('<tr><td><b>%s</b></td><td>%s</td></tr>\n<tr><td>%s</td><td><b>%s</b></td></tr> \n' %
                        (event["name"], '</td><td>'.join(rooml), event["time"], '</b></td><td><b>'.join(namel)))
            for i in range(0, len(block_m)-1):
                lin.append('\\midrule\n')
                row = [' \\newline '.join(d[block_m[j][i]]) for j in range(0, len(block_m))]
                rtml = [' <br/> '.join(d[block_m[j][i]]) for j in range(0, len(block_m))]
                ctml = [x.replace('\\textbf{', '<a href="abstracts#'+str(block_m[j][i])+'">').replace('}', '</a>') for x in rtml]
                lin.append(' & %s \\\\' % ' & '.join(row))
                ltml.append('<tr><td></td><td>%s</td></tr> \n' % '</td><td>'.join(ctml))
        else:  # Break etc.
            lin.append('\\midrule \n %s & \\textbf{%s} \\\\' % (event["time"], event["name"]))
            ltml.append('<tr><td>%s</td><td><b>%s</b></td></tr> \n' % (event["time"], event["name"]))
    agd_to_html(['<table>\n']+ltml+['</table>'])
    return agt('lp{3.5cm}p{3.5cm}p{3.5cm}p{3.5cm}p{3.5cm}', '\n'.join(lin))


def get_refs():
    """
    Constructs the references from an itemized LaTeX list with
    pagerefs and the _raw_ references extracted from the
    abstracts in format_text, put in bib.

    :return: str LaTeX list of references
    """
    global bib
    bib = OD(sorted(bib.items(), key=lambda (k, v): v))
    bibt = '\\chapter*{References} \n\\begin{itemize} \n'
    for tup, cit in bib.iteritems():
        bibt += '\\item[\\pageref{'+tup[1]+'}] '+cit+'\n'
    bibt += '\n \\end{itemize}'
    return bibt


# TODO: check if this namel tuple makes any sense (used more as string than tuple?)
def clean_info(title, namel):
    """
    This will format the title and authors for the conference
    programme in the desired format.

    :param title: str abstract title
    :param namel: str author names
    :return: str LaTeX conference programme info
    """
    if len(namel) > 5:
        namel = namel[:5]
        namel.append('et. al')
    namel = ', '.join(namel)
    title = '\\textbf{'+title.replace(' \\\\ ', ' ')+'}'
    return title, namel


def tex(ti, tr, na, te):
    """
    This is the main building table for each abstract, being a
    centered figure with a title, a block for page and ToC
    reference, a table of authors, and the content of the
    abstract.

    :param ti: str title with // for breaks
    :param tr: str list with pagerefs and custom
               toc entries from format_toc
    :param na: str table with authors from format_table
    :param te: str sanitized text from format_tex
    :return: str abstract page in LaTeX
    """
    return '''
    \\newpage

    \\begin{figure}[t!]
    \\centering
    \\large\\textbf{%s}
    \\vspace*{0.5cm}
    \\end{figure}
    %s
    %s
    %s ''' % (ti, tr, na, te)


def divide_abstracts(ad):
    key, pres, demo, post = [], [], [], []
    for v in OD(sorted(ad.items(), key=lambda t: t[0])).itervalues():
        if 'keynote' in v[0]:
            key.append(v[1])
        elif 'presentation' in v[0]:
            pres.append(v[1])
        elif 'demo' in v[0]:
            demo.append(v[1])
        elif 'poster' in v[0]:
            post.append(v[1])
    return key, pres, demo, post


def agd_to_html(lin):
    o = open('./abstracts.html', 'ab+')
    o.write('\n'.join(lin).encode('utf-8'))


def html_abst(aid, title, authors, abstract):
    return """
        <a name="%s">
        <div style="background-color: #411939; color: white; padding-left: 5px;">
            <h4>%s</h4>
            %s
        </div>
        %s \n\n""" % (aid, title, authors, abstract)


def xml_to_html(d):
    d = OD(sorted(d.items(), key=lambda (k, v): v[0]))
    o = open('./abstracts.html', 'ab+')
    for aid, infl in d.iteritems():
        o.write(html_abst(str(aid), infl[0], ', '.join(infl[1]), infl[2]).encode("utf-8"))


def main():

    tree = ET.parse('../static/abstracts.xml')
    submissions = tree.getroot()
    abstract_dict, agenda_dict, html_dict = {}, {}, {}

    for submission in submissions:
        if 'REJECT' not in submission[3].text and int(submission.attrib['id']) not in retr:

            submission_id = int(submission.attrib['id'])
            # keywords = [k.text for k in submission[1]]
            decision = submission[3].text
            title = format_title(submission[0].text)
            names = [(sanitize(entry[0].text), lower_dutch_prep(entry[1].text)) for entry in submission[4]]
            namel = [(sanitize(entry[0].text) + ' ' + lower_dutch_prep(entry[1].text)) for entry in submission[4]]
            afilliations = [sanitize(entry[3].text) for entry in submission[4]]
            mails = [(sanitize(entry[2].text) if entry[2].text else '') for entry in submission[4]]

            abstract = tex(title, format_text(submission[2].text, title),
                           format_toc(title, names), format_table(names, afilliations, mails))

            abstract_dict[submission[0].text] = (decision, abstract)
            agenda_dict[submission_id] = (clean_info(title, namel))  # TODO: clean that out earlier
            html_dict[submission_id] = [submission[0].text, namel, submission[2].text.replace('\n', '<br/>')]
            for entry in retr:  # TODO: check if this is still needed
                agenda_dict[entry] = ('', '')

    key, pres, demo, post = divide_abstracts(abstract_dict)
    with open('../tex/bos_i.tex', 'r') as i:
        o = open('../tex/bos_o.tex', 'w')
        i = i.read()
        # i = i.replace('% agenda', get_agenda(agenda_dict).encode("utf-8"))
        # i = i.replace('% keynote', '\n'.join(key).encode("utf-8"))
        i = i.replace('% abstracts', '\n'.join(pres).encode("utf-8"))
        # i = i.replace('% demos', '\n'.join(demo).encode("utf-8"))
        # i = i.replace('% posters', '\n'.join(post).encode("utf-8"))
        # i = i.replace('% refl', get_refs().encode("utf-8"))
        o.write(i)
        o.close()
    xml_to_html(html_dict)

if __name__ == '__main__':
    main()
