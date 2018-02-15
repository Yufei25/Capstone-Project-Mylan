# Capstone-Project-Mylan
Capstone project - Mylan

## Introduction
This is a NLP project for contract review extracting. Please check this document if you have any doubt about the logic of the algorithm or the effects of each function and variable

The project has mainly three module:

#### 1. search
This module locates the terms(keywords) in the documents
#### 2. find_pattern
This module extract the pattern names of terms(keywords)
#### 3. match_pattern
This module finds next index of paragraph that has the same pattern of terms(keywords). The pattern of terms(keywords) are extracted in module 2 as mentioned above. 

## Functions:

#### 1. search
search()
#### 2. find_pattern
>The following functions will return true is the input keyword has the given pattern

>input: keyword = keyword

>output: True/False

* indent() 

	This function will return a number represent the length of indent
* bold()
* italic()
* underline()
* double_quotes()
* single_quotes()
* upper_case()
* upper_camel_case()
* bullet_pattern()

>The following functions will return true is the paragraph has the given pattern

>input: 
>paragraph = the content of one paragraph,
>keyword = keyword

>output: True/False

* is_indent()
* isListPara()
* is_bold()
* is_italic()
* is_underline()
* is_double_quotes()
* is_single_quotes()
* is_upper_case()
* is_upper_camel_case()
* is_bullet_pattern()


#### 3. match_pattern
* match()

* find_patterns()

* remove_stopwords()

* contains_sliding_window()


