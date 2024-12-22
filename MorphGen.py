# main order of program:
"""root (strong/weak)
    strong: none of the letters ܐ ܘ ܝ
        regular ("healthy"); vowel on C2 varies from verb to verb (a/u, e/a, a/a, a/e, e/u)
        1-sibilant
        1-nun (different future)
        3-guttural/rish
    weak: at least one of the letters ܐ ܘ ܝ
        1-olaph
        2-olaph
        3-olaph (object pronouns suffix differently)
        1-yodh
        2-waw/yodh
    geminate (C2 = C3)
    irregular (7-8, including two 4-consonant roots)
--> "measure/pattern/template/form/stem/conjugation" (binyan)
    p'al:   basic; vowel on C2 usually "a" or "e"
    pa'el:  intensive
    aph'el: causative
    passive counterpart for all of the above, with "eth-" prefix
        ethp'el:    passive of p'al
        ethpa'al:   passive of pa'el
        ettaph'al:  passive of aph'el
--> TAM
    perfect ~ past
    imperfect ~ future
    active participle ~ present
    imperative (orders)
    passive participle
    infinitive
--> number/person/gender
    number: singular / plural
    person: 1st / 2nd / 3rd
    gender: masculine / feminine / common"""


# verbal root weaknesses
"""3-olaph:
    remove final olaph for any non-null ending in perfect
    3fp has ending of final yodh, so no olaph here
    in ethp'el, pa'el, ethpa'al, aph'el: 3-olaph becomes yodh
    (merges in these cases with 3-yodh, which has regular consonants)
    ettaph'al regular?"""

"""2-waw:
    remove medial waw throughout perfect
    no irregularities for pa'el?
    ethp'el = ettaph'al?
    """

"""geminate:
    only one consonant represented in p'al, aph'el
    no other irregularities?"""



# dictionary template for indicative forms: perfect, imperfect, and participles
# iterates over numbers, persons, and genders
# boolean "is_part" triggers separate masculine and feminine forms in the first person
def indic_template(is_part = False):
    blank = {}
    for number in ['s', 'p']: # singular/plural
        for person in range(3, 0, -1): # 3rd/2nd/1st
            if person == 1 and not is_part: # common gender only in the first person of non-participial forms
                pgn = str(person) + 'c' + number
                blank[pgn] = '' # adds person/gender/number key with empty value
            else:
                for gender in ['m', 'f']: # masculine/feminine
                    pgn = str(person) + gender + number
                    blank[pgn] = ''
    return blank
# alternative structure: nested dictionaries, to display as a table

# blank template for a conjugation pattern
# returns a dictionary of dictionaries, one for each TAM value
# implemented as a function because otherwise, referencing it multiple times only overwrites the same paradigm
def conj_template():
    return {
        "perfect" : {},
        "imperfect" : {},
        "imperative" : {},
        "infinitive" : {},
        "active participle" : {},
        "passive participle" : {}
    }

# blank template for a full verb
# returns a dictionary of dictionaries (of dictionaries), one for each measure/conjugation
# implemented as a function due to peer pressure (cf. above)
def verb_template():
    return {
        "p'al" : {},
        "ethp'el" : {},
        'pa"el' : {},
        'ethpa"al' : {},
        "aph'el" : {},
        "ettaph'al" : {}
    }



# add reflexive prefix (ethp'el, ethpa"al, ettaph'al)
def refl_pref(root):
    return 'ܐܬ' + root # elsewhere, the olaph will be removed in the imperfect, infinitive, and participles



# add perfect endings
def perfect(stem):
    perf_paradigm = indic_template() # use indicative template
    # populate with forms
    perf_paradigm['3ms'] = stem
    perf_paradigm['3fs'] = stem + 'ܬ'
    perf_paradigm['2ms'] = stem + 'ܬ'
    perf_paradigm['2fs'] = stem + 'ܬܝ'
    perf_paradigm['1cs'] = stem + 'ܬ'
    perf_paradigm['3mp'] = stem + 'ܘ' + ' / ' + stem + 'ܘܢ' # optional nunation
    perf_paradigm['3fp'] = stem + ' / ' + stem + 'ܝ' + ' / ' + stem + 'ܝܢ' # 3 forms here
    perf_paradigm['2mp'] = stem + 'ܬܘܢ'
    perf_paradigm['2fp'] = stem + 'ܬܝܢ'
    perf_paradigm['1cp'] = stem + 'ܢ' + ' / ' + stem + 'ܢܢ'
    return perf_paradigm


# add imperfect affixes
def imperfect(stem, vowel):
    # need to add waw if the inherent vowel is /u/
    if vowel == 'u':
        l_stem = stem[:2] + 'ܘ' + stem[2] # don't need to worry about indexing from both sides because all 4-consonant roots are a/e
    else:
        l_stem = stem

    imperf_paradigm = indic_template() # use indicative template
    # populate with forms
    imperf_paradigm['3ms'] = 'ܢ' + l_stem
    imperf_paradigm['3fs'] = 'ܬ' + l_stem + ' / ' + 'ܬ' + l_stem + 'ܝ' + ' (rare)'
    imperf_paradigm['2ms'] = 'ܬ' + l_stem
    imperf_paradigm['2fs'] = 'ܬ' + stem + 'ܝܢ' # shortened stem (no vowel after C2) for any ending that is pronounced (not 'y')
    imperf_paradigm['1cs'] = 'ܐ' + l_stem
    imperf_paradigm['3mp'] = 'ܢ' + stem + 'ܘܢ'
    imperf_paradigm['3fp'] = 'ܢ' + stem + 'ܢ'
    imperf_paradigm['2mp'] = 'ܬ' + stem + 'ܘܢ'
    imperf_paradigm['2fp'] = 'ܬ' + stem + 'ܢ'
    imperf_paradigm['1cp'] = 'ܢ' + l_stem

    # for the ettaph'al specifically, need to reduce all instances of triple-taw
    for form in imperf_paradigm:
        if 'ܬܬܬ' in imperf_paradigm[form]:
            imperf_paradigm[form] = imperf_paradigm[form].replace('ܬܬܬ', 'ܬܬ') # replace every instance of 3 taws with two taws (see below for what really happens)
            # with vowels, it is more apparent that the second taw is dropped (actually, written without doubling as the third taw)
    # concern: is this an orthographic process that also applies to verbs with taw-initial roots in any reflexive conjugation? right now it would apply...

    return imperf_paradigm


# add imperative affixes
def imperative(stem, vowel):

    # need to add waw if the inherent vowel is /u/ (as in imperfect)
    if vowel == 'u':
        l_stem = stem[:2] + 'ܘ' + stem[2]
    else:
        l_stem = stem

    return {
        '2ms' : l_stem,
        '2fs' : l_stem + 'ܝ' + ' / ' + l_stem + 'ܝܢ',
        '2mp' : l_stem + 'ܘ' + ' / ' + l_stem + 'ܘܢ',
        '2fp' : l_stem + 'ܝ' + ' / ' + l_stem + 'ܝܢ'
    }


# make infinitive; this is the only function to return a string rather than a dictionary (because there is no inflection)
def infinitive(stem, conj = "not p'al"):

    # w-suffix, for all conjugations except p'al
    if conj != "p'al":
        stem += 'ܘ'

    return 'ܡ' + stem


# add participle endings
def part_ends(stem, conj = "not p'al"):

    # m-prefix, for all conjugations except p'al
    if conj != "p'al":
        stem = 'ܡ' + stem

    # create base adjectival forms
    ms = stem
    fs = stem + 'ܐ'
    mp = stem + 'ܝܢ'
    fp = stem + 'ܢ'

    part_paradigm = indic_template(True)
    # now add clitic pronouns
    part_paradigm['3ms'] = ms
    part_paradigm['3fs'] = fs
    part_paradigm['2ms'] = ms + ' ܐܢܬ' + ' / ' + ms + 'ܬ'
    part_paradigm['2fs'] = fs + ' ܐܢܬܝ' + ' / ' + fs[:-1] + 'ܬܝ' # non-ms contracted forms remove final consonant
    part_paradigm['1ms'] = ms + ' ܐܢܐ' + ' / ' + ms + 'ܢܐ'
    part_paradigm['1fs'] = fs + ' ܐܢܐ' + ' / ' + fs[:-1] + 'ܢܐ'
    part_paradigm['3mp'] = mp
    part_paradigm['3fp'] = fp
    part_paradigm['2mp'] = mp + ' ܐܢܬܘܢ' + ' / ' + mp[:-1] + 'ܬܘܢ'
    part_paradigm['2fp'] = fp + ' ܐܢܬܝܢ' + ' / ' + fp[:-1] + 'ܬܝܢ'
    part_paradigm['1mp'] = mp + ' ܚܢܢ' + ' / ' + mp[:-1] + 'ܢܢ'
    part_paradigm['1fp'] = fp + ' ܚܢܢ' + ' / ' + fp[:-1] + 'ܢܢ'

    return part_paradigm



# returns p'al dictionary
# this is the only conjugation generator that takes multiple arguments, due to the inherent perf/imp vowels
# without specification, verbs by default have 'a' in the perfect and 'u' in the imperfect
# NB that because no vowels are displayed right now, the perfect vowel arg doesn't have any effect currently
def conj1(root, perf_V = 'a', imp_V = 'u'):
    conj = conj_template()

    conj["perfect"] = perfect(root)
    conj["imperfect"] = imperfect(root, imp_V)
    conj["imperative"] = imperative(root, imp_V)
    # NB that all of the following conjugations call the TAM function with 'conj = "p'al"'
    # because the p'al is formed differently from all other conjugations
    # (no w-suffix infinitive, no m-prefix participle
    conj["infinitive"] = infinitive(root, conj = "p'al")
    conj["active participle"] = part_ends(root, conj = "p'al")
    pass_part_stem = root[:2] + 'ܝ' + root[2] # infix 'y' for the p'al passive participle only
    conj["passive participle"] = part_ends(pass_part_stem, conj = "p'al")

    return conj


# returns ethp'el dictionary
def conj2(root):
    conj = conj_template()

    # add 'eth-' to make stem
    # (olaph to be removed from imperfect, infinitive, passive participle)
    refl_stem = refl_pref(root)

    # now generate forms using this reflexive stem
    conj["perfect"] = perfect(refl_stem)
    conj["imperfect"] = imperfect(refl_stem[1:], 'e') # removing olaph from stem
    conj["imperative"] = imperative(refl_stem, 'e')
    conj["infinitive"] = infinitive(refl_stem[1:]) # removing olaph from stem
    # NO ACTIVE PARTICIPLE -- cf. how blank dictionaries are displayed
    conj["passive participle"] = part_ends(refl_stem[1:]) # removing olaph from stem

    return conj


# return pa"el dictionary
def conj3(root):
    conj = conj_template()

    conj["perfect"] = perfect(root)
    conj["imperfect"] = imperfect(root, 'e')
    conj["imperative"] = imperative(root, 'e')
    conj["infinitive"] = infinitive(root)
    # NB that in the pa"el the active and passive participles have exactly the same consonants
    # furthermore, all non-ms forms are exactly the same, down to the vowels
    conj["active participle"] = part_ends(root)
    conj["passive participle"] = part_ends(root)

    return conj


# return ethpa"al dictionary
def conj4(root):
    # NB that the forms of the ethpa"al have exactly the same consonants as the ethp'el and differ only in vowels and vowel placement
    # so until vowels are fully added, the one function will call the other
    return conj2(root)


# return aph'el dictionary
def conj5(root):
    conj = conj_template()

    # add causative olaph prefix, to make stem
    # (olaph to be removed from imperfect, infinitive, and BOTH active/passive participles)
    caus_stem = 'ܐ' + root

    # now generate forms using this causative stem
    conj["perfect"] = perfect(caus_stem)
    conj["imperfect"] = imperfect(caus_stem[1:], 'e') # removing olaph from stem
    conj["imperative"] = imperative(caus_stem, 'e')
    conj["infinitive"] = infinitive(caus_stem[1:]) # removing olaph from stem
    # NB that in the aph'el the active and passive participles have exactly the same consonants
    # furthermore, all non-ms forms are exactly the same, down to the vowels
    conj["active participle"] = part_ends(caus_stem[1:]) # removing olaph from stem
    conj["passive participle"] = part_ends(caus_stem[1:]) # removing olaph from stem

    return conj


# return ettaph'al dictionary
def conj6(root):
    conj = conj_template()

    # prefix '-t-' and then reflexive 'eth-' to make stem
    # (olaph to be removed from imperfect, infinitive, and passive participles)
    stem = refl_pref('ܬ' + root)

    # now generate forms using this stem
    conj["perfect"] = perfect(stem)
    conj["imperfect"] = imperfect(stem[1:], 'a') # removing olaph from stem
    conj["imperative"] = imperative(stem, 'a')
    conj["infinitive"] = infinitive(stem[1:]) # removing olaph from stem
    # NO ACTIVE PARTICIPLE -- cf. how blank dictionaries are displayed
    conj["passive participle"] = part_ends(stem[1:]) # removing olaph from stem

    return conj



# generate full verb conjugation dict
# requires root, list of measures/conjugations, and perfect/imperfect/imperative vowels for p'al
# by default, a verb exists in all 6 measures/conjugations unless limited
# so too, default vowels for p'al are passed as 'a' (perf) and 'u' (imp)
def full_verb_conj(root, conj_list = [1, 2, 3, 4, 5, 6], perf_V = 'a', imp_V = 'u'):
    conj = verb_template()

    # any condition not triggered will leave an empty paradigm, which will be rendered with a note to this effect
    if 1 in conj_list:
        conj["p'al"] = conj1(root, perf_V, imp_V)
    if 2 in conj_list:
        conj["ethp'el"] = conj2(root)
    if 3 in conj_list:
        conj['pa"el'] = conj3(root)
    if 4 in conj_list:
        conj['ethpa"al'] = conj4(root)
    if 5 in conj_list:
        conj["aph'el"] = conj5(root)
    if 6 in conj_list:
        conj["ettaph'al"] = conj6(root)

    return conj



# NB: the two items below are DONE, cxu ne?
# display forms in a list (add functionality for 2D tables?)
# with current structure, could make the program recursive
def disp_table(content, num_tabs = 0, label = 'full paradigm'):
    if type(content) == type({}): # check as dictionary
        if content == {}: # check for empty dictionary, in which case explain that forms don't exist
            print('\t' * num_tabs + 'NO ' + label.upper())
        else:
            print('\t' * num_tabs + label + ':')
            for item in content:
                disp_table(content[item], num_tabs + 1, item) # recurse but with one more indentation
    elif type(content) == type(''): # check as string
        print('\t' * num_tabs + label + ':\t' + content) # for displaying individual forms
    else: # any other type
        print("ERROR: CONTENT/PARADIGM TYPE NOT RECOGNIZED")



# demonstrate full verb conjugation, asking questions/input of user
def demo():
    root = input("What is the verb root?")

    conjs = input("""
In which 'measures' does this verb occur?
    1 = p'al
    2 = ethp'el
    3 = pa"el
    4 = ethpa"al
    5 = aph'el
    6 = ettaph'al
(type all that apply)"""
    )
    conj_list = []
    for num in conjs:
        conj_list.append(int(num))

    # just setting some defaults before soliciting user input
    perf_vowel = 'a'
    imp_vowel = 'u'
    if 1 in conj_list:  # ask specific questions about p'al
        print("In the p'al...")
        perf_vowel = input("\t...what is the inherent vowel in the perfect? (a/e)")
        imp_vowel = input("\t...what is the inherent vowel in the imperfect/imperative? (u/a/e)")

    disp_table(full_verb_conj(root, conj_list, perf_vowel, imp_vowel))


demo()




"""
next questions:
- ask how multiple forms should be handled--say, as a list that is the value to the given key?
- does the triple-taw rule apply to taw-initial roots in any reflexive conjugation?

next steps:
- write unit tests
- extend functionality to root irregularities

more questions:
- should the "conj1-6" functions be refactored to be instances of a single conjugation function,
    where (e.g.) even/passive conjugations automatically lack active participles,
    so that there is one abstract act of conjugation?
"""