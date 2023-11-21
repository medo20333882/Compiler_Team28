import tkinter as tk
from enum import Enum
import re
import pandas
import pandastable as pt
from nltk.tree import *


class Token_type(Enum):
    program = 1
    end = 2
    integer = 3
    real = 4
    complex = 5
    logical = 6
    If = 7
    character = 8
    parameter = 9
    then = 10
    Else = 11
    do = 12
    read = 13
    print = 14
    EqualOp = 15
    LessThanOp = 16
    GreaterThanOp = 17
    NotEqualOp = 18
    PlusOp = 19
    MinusOp = 20
    MultiplyOp = 21
    DivideOp = 22
    RParenthesis = 23
    LParenthesis = 24
    Colon = 25
    STR_VALUE = 26
    GreaterThanOrEqualOp = 27
    LessThanOrEqualOp = 28
    EqualEqualOp = 29
    Identifier = 30
    Number = 31
    Error = 32
    Dot = 33
    comma = 34
    IMPLICIT = 35
    NONE = 36
    Len = 37
    true = 38
    false = 39
    comment = 40


# class token to hold string and token type
class token:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def to_dict(self):
        return {
            'Lex': self.lex,
            'token_type': self.token_type
        }


List = []
split_chars = []  # to hold one by one character
Tokens = []  # To hold the real tokens
errors = []  # To hold errors


Keywords = {"program": Token_type.program,
            "end": Token_type.end,
            "integer": Token_type.integer,
            "real": Token_type.real,
            "complex": Token_type.complex,
            "logical": Token_type.logical,
            "character": Token_type.character,
            "parameter": Token_type.parameter,
            "if": Token_type.If,
            "then": Token_type.then,
            "else": Token_type.Else,
            "do": Token_type.do,
            "read*": Token_type.read,
            "print*": Token_type.print,
            "implicit": Token_type.IMPLICIT,
            "none": Token_type.NONE,
            "len": Token_type.Len,
            "true": Token_type.true,
            "false": Token_type.false
            }
RelationalOperator = {">": Token_type.GreaterThanOp,
                      "<": Token_type.LessThanOp,
                      "<=": Token_type.GreaterThanOrEqualOp,
                      ">=": Token_type.LessThanOrEqualOp,
                      "==": Token_type.EqualEqualOp,
                      "/=": Token_type.NotEqualOp
                      }
ArithmeticOperators = {"=": Token_type.EqualOp,
                       "+": Token_type.PlusOp,
                       "-": Token_type.MinusOp,
                       "*": Token_type.MultiplyOp,
                       "/": Token_type.DivideOp
                       }
Symbols = {":": Token_type.Colon,
           "(": Token_type.LParenthesis,
           ")": Token_type.RParenthesis,
           ".": Token_type.Dot,
           ",": Token_type.comma
           }
Comment={"!": Token_type.comment}


def find_token(word):
    if word in Keywords:
        print(word + " is Keywords")
        Tokens.append(token(word, Keywords[word]))
    elif word in RelationalOperator:
        print(word + " is RelationalOperator")
        Tokens.append(token(word, RelationalOperator[word]))
    elif word in ArithmeticOperators:
        print(word + " is ArithmeticOperators")
        Tokens.append(token(word, ArithmeticOperators[word]))
    elif word in Symbols:
        print(word + " is Symbols")
        Tokens.append(token(word, Symbols[word]))
    elif re.match("^([0-9]+(\.[0-9]*)?|\.[0-9]+)$", word):
        print(word + " is Number")
        Tokens.append(token(word, Token_type.Number))
    elif re.match("^[a-zA-Z]|[a-zA-Z0-9]*$", word):
        print(word + " is Identifier")
        Tokens.append(token(word, Token_type.Identifier))
    elif (word.startswith("\"") and word.endswith("\"")) \
            or (word.startswith("'") and word.endswith("'")):
        print(word + " is String Value")
        Tokens.append(token(word, Token_type.STR_VALUE))
    elif word.startswith("!"):
        print(word + " is Comment")
    else:
        Tokens.append(token(word, Token_type.Error))
        errors.append("Lexical error  " + word)


def split(text):
    flag1 = False
    flag2 = False
    flag3 = False
    flag4 = False
    num = 0
    for i in text:
        split_chars.append(i)
    for k in split_chars:
        num = num + 1
        if k=="\n":
            continue
        elif k == "\"" or k == "'" or flag1:
            flag1 = True
            if num - 1 == len(split_chars) - 1 or split_chars[num] == "\"" \
                    or split_chars[num] == "'":
                List.append(k)
                List.append(split_chars[num])
                string = ''.join(List)
                find_token(string)
                split_chars.pop(num)
                flag1 = False
                List.clear()
            else:
                List.append(k)
        elif k =="!" or flag4:
            flag4=True
            if num - 1 == len(split_chars) - 1 or split_chars[num]=="\n":
                List.append(k)
                my_string = ''.join(List)
                find_token(my_string)
                List.clear()
                flag4=False
            else:
                List.append(k)
        elif re.match("^[a-zA-Z]*$", k) or flag2:
            if num-1 == len(split_chars) - 1 or split_chars[num] == "_" or\
                    re.match("^[0-9]$", split_chars[num]):
                flag2 = True
            if num - 1 == len(split_chars) - 1 or split_chars[num] == " " \
                    or split_chars[num] in RelationalOperator or split_chars[num] \
                    in ArithmeticOperators or split_chars[num] in Symbols or split_chars[num]=="\n":
                List.append(k)
                my_string = ''.join(List)
                if (my_string == "print" or my_string == "read") and split_chars[num] == "*":
                    my_string = my_string + "*"
                    split_chars.pop(num)
                elif (my_string == "print" or my_string == "read") and (
                        split_chars[num] == " " and split_chars[num + 1] == "*"):
                    my_string = my_string + "*"
                    split_chars.pop(num + 1)
                find_token(my_string)
                List.clear()
                flag2 = False
            else:
                List.append(k)
        elif re.match("^[0-9]$", k) or flag3:
            if num - 1 == len(split_chars) - 1 or split_chars[num] == ".":
                flag3 = True
            if num - 1 == len(split_chars) - 1 or split_chars[num] == " " or split_chars[num] in\
                    RelationalOperator or split_chars[num] in ArithmeticOperators or re.match(
                "^[a-z]$", split_chars[num]) or split_chars[num] == ")" or split_chars=="," or split_chars[num]=="\n":
                List.append(k)
                my_string = ''.join(List)
                find_token(my_string)
                List.clear()
                flag3 = False
            else:
                List.append(k)
        elif k in Symbols or k in RelationalOperator or k in ArithmeticOperators:
            if k == "<" or k == ">" or k == "=":
                if not split_chars[num] == "=":
                    find_token(k)
                else:
                    List.append(k)
                    List.append(split_chars[num])
                    my_string = ''.join(List)
                    find_token(my_string)
                    List.clear()
                    split_chars.pop(num)
            else:
                find_token(k)
        elif k == " ":
            continue
        else:
            List.append(k)
            my_string = ''.join(List)
            find_token(my_string)


def Parse():
    j = 0
    Children = []

    # Parse Header
    Header_dict = Header(j)
    Children.append(Header_dict["node"])
    j = Header_dict["index"]

    # Parse Block
    Block_dict = Block(j)
    Children.append(Block_dict["node"])
    j = Block_dict["index"]

    # Parse Footer
    Footer_dict = Footer(j)
    Children.append(Footer_dict["node"])
    j = Footer_dict["index"]

    Node = Tree('Program', Children)
    return Node


def Header(j):
    output = dict()
    # To check at Token program
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.program:
        program_output = Match(Token_type.program, j)
        j = program_output["index"]

        # To check at Token Identifier
        identifier_output = Match(Token_type.Identifier, j)
        j = identifier_output["index"]

        # To check at Token Implicit
        implicit_output = Match(Token_type.IMPLICIT, j)
        j = implicit_output["index"]

        # To check at Token None
        none_output = Match(Token_type.NONE, j)
        j = none_output["index"]
        output["node"] = Tree("Header", [program_output["node"], identifier_output["node"]
            , implicit_output["node"], none_output["node"]])
        output["index"] = j
        return output

    else:
        output["node"] = Tree("error", [])
        output["index"] = j
        return output


def Block(j):
    output = dict()
    Decl_Output = DeclSec(j)
    j = Decl_Output["index"]
    Assign_Output = AssignVals(j)
    j = Assign_Output["index"]
    Stmts_Output = Statements(j)
    j = Stmts_Output["index"]
    output["node"] = Tree("Block", [Decl_Output["node"], Assign_Output["node"], Stmts_Output["node"]])
    output["index"] = j
    return output


def DeclSec(j):
    output = dict()
    constdecls_output = ConstDecls(j)
    j = constdecls_output["index"]
    VarDecls_output = VarDecls(j)
    j = VarDecls_output["index"]
    output["node"] = Tree("DeclSec", [constdecls_output["node"], VarDecls_output["node"]])
    output["index"] = j
    return output


def ConstDecls(j):
    output = dict()
    constdecl_out = ConstDecl(j)
    j = constdecl_out["index"]
    Temp1 = Tokens[j].to_dict()
    Temp2 = Tokens[j + 1].to_dict()
    if (Temp1['token_type'] != Token_type.integer) and \
            (Temp1['token_type'] != Token_type.real) and \
            (Temp1['token_type'] != Token_type.character):
        output["node"] = Tree("ConstDecls", [constdecl_out["node"]])
        output["index"] = j
        return output

    elif Temp1['token_type'] == Token_type.integer or \
            Temp1['token_type'] == Token_type.real or Temp1['token_type'] == Token_type.character:
        if Temp2['token_type'] == Token_type.comma:
            constdecls_out = ConstDecls(j)
            output["node"] = Tree("ConstDecls", [constdecl_out["node"], constdecls_out["node"]])
            j = constdecls_out["index"]
            output["index"] = j
            return output

        else:
            output["node"] = Tree("ConstDecls", [constdecl_out["node"]])
            output["index"] = j
            return output

    else:
        output["node"] = Tree("epsilon", [])
        output["index"] = j
        return output


def ConstDecl(j):
    output = dict()
    Temp1 = Tokens[j].to_dict()
    Temp2 = Tokens[j+1].to_dict()
    if Temp1['token_type'] == Token_type.integer or \
            Temp1['token_type'] == Token_type.real:
        if Temp2["token_type"]==Token_type.comma:
            datatype_output = Datatype(j)
            j = datatype_output["index"]
            # To check at Token comma
            comma_output = Match(Token_type.comma, j)
            j = comma_output["index"]
            # To check at Token Parameter
            parameter_output = Match(Token_type.parameter, j)
            j = parameter_output["index"]
            # To check at Token Colon
            colon1_output = Match(Token_type.Colon, j)
            j = colon1_output["index"]
            # To check at Token Colon
            colon2_output = Match(Token_type.Colon, j)
            j = colon2_output["index"]
            # To check at Token Identifier
            identifier_output = Match(Token_type.Identifier, j)
            j = identifier_output["index"]
            # To check at Token Equal
            equal_output = Match(Token_type.EqualOp, j)
            j = equal_output["index"]
            value_output = Value(j)
            j = value_output["index"]
            output["node"] = Tree("ConstDecl", [datatype_output["node"], comma_output["node"]
                , parameter_output["node"], colon1_output["node"], colon2_output["node"], identifier_output["node"],
                                                equal_output["node"], value_output["node"]])
            output["index"] = j
            return output
        else:
            output["node"] = Tree("epsilon", [])
            output["index"] = j
            return output
    else:

        output["node"] = Tree("error", [])
        output["index"] = j
        return output


def VarDecls(j):
    output = dict()
    vardecl_out = VarDecl(j)
    j = vardecl_out["index"]
    Temp1 = Tokens[j].to_dict()
    Temp2 = Tokens[j + 1].to_dict()
    if (Temp1['token_type'] != Token_type.integer) and \
            (Temp1['token_type'] != Token_type.real) and \
            (Temp1['token_type'] != Token_type.character):
        output["node"] = Tree("VarDecls", [vardecl_out["node"]])
        output["index"] = j
        return output

    elif Temp1['token_type'] == Token_type.integer or \
            Temp1['token_type'] == Token_type.real or Temp1['token_type'] == Token_type.character:
        if Temp2['token_type'] == Token_type.Colon:
            vardecls_out = VarDecls(j)
            output["node"] = Tree("VarDecls", [vardecl_out["node"], vardecls_out["node"]])
            j = vardecls_out["index"]
            output["index"] = j
            return output

        else:
            output["node"] = Tree("VarDecls", [vardecl_out["node"]])
            output["index"] = j
            return output

    else:
        output["node"] = Tree("epsilon", [])
        output["index"] = j
        return output


def VarDecl(j):
    output = dict()
    Temp1 = Tokens[j].to_dict()
    Temp2= Tokens[j+1].to_dict()
    if Temp1['token_type'] == Token_type.integer or \
            Temp1['token_type'] == Token_type.real:
        if Temp2["token_type"]==Token_type.Colon:
            # To check at Token datatype
            datatype_output = Datatype(j)
            j = datatype_output["index"]

            # To check at Token colon
            colon1_output = Match(Token_type.Colon, j)
            j = colon1_output["index"]

            # To check at Token colon
            colon2_output = Match(Token_type.Colon, j)
            j = colon2_output["index"]

            # To check at Token identifier
            id_output = idList(j)
            j = id_output["index"]
            Temp3=Tokens[j].to_dict()
            if Temp3["token_type"]==Token_type.EqualOp:
                # To check at Token Equal
                EqualOp_output = Match(Token_type.EqualOp, j)
                j = EqualOp_output["index"]
                # To check at Token identifier
                num_output = Match(Token_type.Number, j)
                j = num_output["index"]
                output["node"] = Tree("VarDecl",[datatype_output["node"], colon1_output["node"]
                    ,colon2_output["node"],id_output["node"],EqualOp_output["node"],num_output["node"]])
                output["index"] = j
                return output
            else:
                output["node"] = Tree("VarDecl",
                                      [datatype_output["node"], colon1_output["node"], colon2_output["node"],
                                       id_output["node"]])
                output["index"] = j
                return output
        else:
            output["node"] = Tree("epsilon", [])
            output["index"] = j
            return output
    elif Temp1['token_type'] == Token_type.character:
        # To check at Token character
        character_output = Match(Token_type.character, j)
        j = character_output["index"]
        # To check at Token LParenthesis
        LParenthesis_output = Match(Token_type.LParenthesis, j)
        j = LParenthesis_output["index"]
        # To check at Token Len
        Len_output = Match(Token_type.Len, j)
        j = Len_output["index"]
        # To check at Token EqualOp
        EqualOp_output = Match(Token_type.EqualOp, j)
        j = EqualOp_output["index"]
        # To check at Token Number
        Number_output = Match(Token_type.Number, j)
        j = Number_output["index"]
        # To check at Token RParenthesis
        RParenthesis_output = Match(Token_type.RParenthesis, j)
        j = RParenthesis_output["index"]
        # To check at Token Colon
        colon1_output = Match(Token_type.Colon, j)
        j = colon1_output["index"]
        # To check at Token Colon
        colon2_output = Match(Token_type.Colon, j)
        j = colon2_output["index"]
        # To check at Token Identifier
        identifier_output = Match(Token_type.Identifier, j)
        j = identifier_output["index"]
        output["node"] = Tree("VarDecl", [character_output["node"], LParenthesis_output["node"]
            , Len_output["node"], EqualOp_output["node"], Number_output["node"], RParenthesis_output["node"],
                colon1_output["node"], colon2_output["node"],identifier_output["node"]])
        output["index"] = j
        return output

    else:
        output["node"] = Tree("epsilon", [])
        output["index"] = j
        return output
def idList(j):
    output = dict()
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.Identifier:
        identifier_out = Match(Token_type.Identifier, j)
        j = identifier_out["index"]
        idlistrest_out=idListRest(j)
        j=idlistrest_out["index"]
        output["node"] = Tree("idList", [identifier_out["node"],idlistrest_out["node"]])
        output["index"] = j
        return output
    else:
        output["node"] = Tree("epsilon", [])
        output["index"] = j
        return output


def idListRest(j):
    output = dict()
    Temp = Tokens[j].to_dict()
    if Temp["token_type"]==Token_type.comma:
        comma_output = Match(Token_type.comma, j)
        j = comma_output["index"]
        identifier_out = Match(Token_type.Identifier, j)
        j = identifier_out["index"]
        rest_out = idListRest(j)
        j = rest_out["index"]
        output["node"] = Tree("idListRest", [comma_output["node"], identifier_out["node"],rest_out["node"]])
        output["index"] = j
        return output
    else:
        output["node"] = Tree("epsilon", [])
        output["index"] = j
        return output


def Datatype(j):
    output = dict()
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.integer:
        integer_output = Match(Token_type.integer, j)
        j = integer_output["index"]
        output["node"] = Tree("Datatype", [integer_output["node"]])
        output["index"] = j
        return output

    elif Temp['token_type'] == Token_type.real:
        real_output = Match(Token_type.real, j)
        j = real_output["index"]
        output["node"] = Tree("Datatype", [real_output["node"]])
        output["index"] = j
        return output

    elif Temp['token_type'] == Token_type.character:
        char_output = Match(Token_type.character, j)
        j = char_output["index"]

        lparenthesis_output = Match(Token_type.LParenthesis, j)
        j = lparenthesis_output["index"]

        len_output = Match(Token_type.Len, j)
        j = len_output["index"]

        equal_output = Match(Token_type.EqualOp, j)
        j = equal_output["index"]

        num_output = Match(Token_type.Number, j)
        j = num_output["index"]

        rparenthesis_output = Match(Token_type.RParenthesis, j)
        j = rparenthesis_output["index"]

        output["node"] = Tree("Datatype", [char_output["node"], lparenthesis_output["node"], len_output["node"],
                                           equal_output["node"], num_output["node"], rparenthesis_output["node"]])
        output["index"] = j
        return output

    else:
        output["node"] = Tree("error", [])
        output["index"] = j
        return output


def Value(j):
    output = dict()
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.Number:
        num_output = Match(Token_type.Number, j)
        j = num_output["index"]
        output["node"] = Tree("Value", [num_output["node"]])
        output["index"] = j
        return output

    elif Temp['token_type'] == Token_type.STR_VALUE:
        string_output = Match(Token_type.STR_VALUE, j)
        j = string_output["index"]
        output["node"] = Tree("Value", [string_output["node"]])
        output["index"] = j
        return output

    else:
        output["node"] = Tree("error", [])
        output["index"] = j
        return output


def AssignVals(j):
    output = dict()
    assignval_out = AssignVal(j)
    j = assignval_out["index"]
    Temp1 = Tokens[j].to_dict()
    if (Temp1['token_type'] != Token_type.Identifier) and \
            (Temp1['token_type'] != Token_type.read):
        output["node"] = Tree("AssignVals", [assignval_out["node"]])
        output["index"] = j
        return output

    elif Temp1['token_type'] == Token_type.Identifier or \
            Temp1['token_type'] == Token_type.read:
        assignvals_out = AssignVals(j)
        output["node"] = Tree("AssignVals", [assignval_out["node"], assignvals_out["node"]])
        j = assignvals_out["index"]
        output["index"] = j
        return output

    else:
        output["node"] = Tree("epsilon", [])
        output["index"] = j
        return output


def AssignVal(j):
    output = dict()
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.Identifier:
        identifier_out = Match(Token_type.Identifier, j)
        j = identifier_out["index"]

        equal_out = Match(Token_type.EqualOp, j)
        j = equal_out["index"]

        val_out = Value(j)
        j = val_out["index"]

        output["node"] = Tree("Assignval", [identifier_out["node"], equal_out["node"], val_out["node"]])
        output["index"] = j
        return output

    elif Temp['token_type'] == Token_type.read:
        read_out = Match(Token_type.read, j)
        j = read_out["index"]

        comma_out = Match(Token_type.comma, j)
        j = comma_out["index"]

        identifier2_out = Match(Token_type.Identifier, j)
        j = identifier2_out["index"]

        output["node"] = Tree("Assignval", [read_out["node"], comma_out["node"], identifier2_out["node"]])
        output["index"] = j
        return output

    else:
        output["node"] = Tree("epsilon", [])
        output["index"] = j
        return output


def Statements(j):
    output = dict()
    statement_out = Statement(j)
    j = statement_out["index"]
    Temp1 = Tokens[j].to_dict()
    if (Temp1['token_type'] != Token_type.Identifier) and \
            (Temp1['token_type'] != Token_type.read) and \
            Temp1['token_type'] != Token_type.print and \
            Temp1['token_type'] != Token_type.If and \
            Temp1['token_type'] != Token_type.do and \
            Temp1['token_type'] != Token_type.Number and \
            Temp1['token_type'] != Token_type.LParenthesis:
        output["node"] = Tree("Statements", [statement_out["node"]])
        output["index"] = j
        return output

    elif Temp1['token_type'] == Token_type.Identifier or \
            Temp1['token_type'] == Token_type.read or \
            Temp1['token_type'] == Token_type.print or \
            Temp1['token_type'] == Token_type.If or \
            Temp1['token_type'] == Token_type.do or \
            Temp1['token_type'] == Token_type.Number or \
            Temp1['token_type'] == Token_type.LParenthesis:
        statements_out = Statements(j)
        output["node"] = Tree("Statements", [statement_out["node"], statements_out["node"]])
        j = statements_out["index"]
        output["index"] = j
        return output
    else:
        output["node"] = Tree("epsilon", [])
        output["index"] = j
        return output


def Statement(j):
    output = dict()
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.read:
        # To check at Token read
        read_output = Match(Token_type.read, j)
        j = read_output["index"]
        # To check at Token comma
        comma_output = Match(Token_type.comma, j)
        j = comma_output["index"]
        # To check at Token id
        identifier_output = Match(Token_type.Identifier, j)
        j = identifier_output["index"]
        output["node"] = Tree("Statement", [read_output["node"], comma_output["node"]
            , identifier_output["node"]])
        output["index"] = j
        return output

    elif Temp['token_type'] == Token_type.print:
        # To check at Token print
        print_output = Match(Token_type.print, j)
        j = print_output["index"]
        # To check at Token comma
        comma_output = Match(Token_type.comma, j)
        j = comma_output["index"]
        Temp2 = Tokens[j].to_dict()
        if Temp2["token_type"]==Token_type.Identifier:
            idd_out=idList(j)
            j=idd_out["index"]
            output["node"] = Tree("Statement",[print_output["node"], comma_output["node"]
                 ,idd_out["node"]])
            output["index"] = j
            return output
        else:
            val_output = Value(j)
            j = val_output["index"]
            Temp3 = Tokens[j].to_dict()
            if Temp3["token_type"]==Token_type.comma:
                comma2_output=Match(Token_type.comma,j)
                j=comma2_output["index"]
                idd2_out = idList(j)
                j = idd2_out["index"]
                output["node"] = Tree("Statement", [print_output["node"], comma_output["node"]
                    , val_output["node"],comma2_output["node"],idd2_out["node"]])
                output["index"] = j
                return output
            else:
                output["node"] = Tree("Statement", [print_output["node"], comma_output["node"]
                    , val_output["node"]])
                output["index"] = j
                return output

    elif Temp['token_type'] == Token_type.If:
        # To check at Token if
        if_output = Match(Token_type.If, j)
        j = if_output["index"]
        # To check at Token LParenthesis
        Lp_output = Match(Token_type.LParenthesis, j)
        j = Lp_output["index"]
        # To check at condition
        cond_output = Condition(j)
        j = cond_output["index"]
        # To check at Then
        # To check at Token RParenthesis
        Rp_output = Match(Token_type.RParenthesis, j)
        j = Rp_output["index"]
        then_output = Match(Token_type.then, j)
        j = then_output["index"]
        # To check at Token Statments
        statements_output = Statements(j)
        j = statements_output["index"]
        # To check at Token else_clause
        elseclause_output = ElseClause(j)
        j = elseclause_output["index"]
        output["node"] = Tree("Statement",[if_output["node"], Lp_output["node"],
                cond_output["node"],Rp_output["node"],then_output["node"],
                statements_output["node"],elseclause_output["node"]])
        output["index"] = j
        return output
    elif Temp['token_type'] == Token_type.do:
        # To check at Token do
        do_output = Match(Token_type.do, j)
        j = do_output["index"]
        Temp_next=Tokens[j].to_dict()
        if Temp_next["token_type"] == Token_type.Identifier:
            Temp_comma =Tokens[j+3].to_dict()
            if Temp_comma["token_type"] == Token_type.comma:
                # To check at Token id
                id_output = Match(Token_type.Identifier, j)
                j = id_output["index"]
                # To check at Token equal
                equal_output = Match(Token_type.EqualOp, j)
                j = equal_output["index"]
                # To check at Token integer
                integer_output = Match(Token_type.Number, j)
                j = integer_output["index"]
                # To check at Token comma
                comma1_output = Match(Token_type.comma, j)
                j = comma1_output["index"]
                # To check at Token stop
                stop_output = Stop(j)
                j = stop_output["index"]
                # To check at Token step
                step_output = Step(j)
                j = step_output["index"]
                # To check at Token statements
                statement_output = Statements(j)
                j = statement_output["index"]
                # To check at Token end
                end_output = Match(Token_type.end, j)
                j = end_output["index"]
                # To check at Token do
                do1_output = Match(Token_type.do, j)
                j = do1_output["index"]
                output["node"] = Tree("Statement", [do_output["node"], id_output["node"]
                , equal_output["node"], integer_output["node"], comma1_output["node"]
                , stop_output["node"], step_output["node"],
                                                statement_output["node"], end_output["node"], do1_output["node"]])
                output["index"] = j
                return output
            else:
                #To check at Token statements
                statement_output = Statements(j)
                j = statement_output["index"]
                # To check at Token end
                end_output = Match(Token_type.end, j)
                j = end_output["index"]
                # To check at Token do
                do1_output = Match(Token_type.do, j)
                j = do1_output["index"]
                output["node"] = Tree("Statement", [do_output["node"],
                                                statement_output["node"], end_output["node"], do1_output["node"]])
                output["index"] = j
                return output
        else:
            # To check at Token statements
            statement_output = Statements(j)
            j = statement_output["index"]
            # To check at Token end
            end_output = Match(Token_type.end, j)
            j = end_output["index"]
            # To check at Token do
            do1_output = Match(Token_type.do, j)
            j = do1_output["index"]
            output["node"] = Tree("Statement", [do_output["node"],
                                                statement_output["node"], end_output["node"], do1_output["node"]])
            output["index"] = j
            return output

    elif Temp["token_type"] == Token_type.Identifier or Temp["token_type"] == Token_type.Number \
            or Temp["token_type"] == Token_type.LParenthesis:
        Temp_next = Tokens[j + 1].to_dict()
        if Temp["token_type"] == Token_type.Identifier and Temp_next["token_type"] == Token_type.EqualOp:
            assignment_output = Assignment(j)
            j = assignment_output["index"]
            output["node"] = Tree("Statement", [assignment_output["node"]])
            output["index"] = j
            return output
        else:
            expression_output = Expression(j)
            j = expression_output["index"]
            output["node"] = Tree("Statement", [expression_output["node"]])
            output["index"] = j
            return output

    else:
        output["node"] = Tree("epsilon", [])
        output["index"] = j
        return output

def Assignment(j):
    output = dict()
    id_output =Match(Token_type.Identifier, j)
    j = id_output["index"]

    equal_output = Match(Token_type.EqualOp, j)
    j = equal_output["index"]

    expression_output = Expression(j)
    j = expression_output["index"]

    output["node"] = Tree("Assignment", [id_output["node"], equal_output["node"], expression_output["node"]])
    output["index"] = j
    return output

def Condition(j):
    output = dict()
    Exp1_Output = Expression(j)
    j = Exp1_Output["index"]
    RelOp_Output = RelOp(j)
    j = RelOp_Output["index"]
    Exp2_Output = Expression(j)
    j = Exp2_Output["index"]
    output["node"] = Tree("Condition", [Exp1_Output["node"], RelOp_Output["node"], Exp2_Output["node"]])
    output["index"] = j
    return output


def Expression(j):
    output = dict()
    # To check at Token term
    term_output = Term(j)
    j = term_output["index"]
    # To check at Token AddopExpression
    addopexpression_output = AddOpExpression(j)
    j = addopexpression_output["index"]
    output["node"] = Tree("Expression", [term_output["node"], addopexpression_output["node"]])
    output["index"] = j
    return output


def AddOpExpression(j):
    output = dict()
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.PlusOp or Temp['token_type'] == Token_type.MinusOp:
        # To check at Token addop
        addop_output = AddOp(j)
        j = addop_output["index"]
        # To check at Token term
        term_output = Term(j)
        j = term_output["index"]
        # To check at Token addopexpression
        addopexpression_output = AddOpExpression(j)
        j = addopexpression_output["index"]
        output["node"] = Tree("AddOpExpression", [addop_output["node"],
                                                  term_output["node"], addopexpression_output["node"]])
        output["index"] = j
        return output
    else:
        output["node"] = Tree("epsilon", [])
        output["index"] = j
        return output


def Term(j):
    output = dict()
    # To check at Token Factor
    factor_output = Factor(j)
    j = factor_output["index"]
    # To check at Token Multiopterm
    multiopterm_output = MultOpTerm(j)
    j = multiopterm_output["index"]
    output["node"] = Tree("Term", [factor_output["node"], multiopterm_output["node"]])
    output["index"] = j
    return output


def MultOpTerm(j):
    output = dict()
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.DivideOp or Temp['token_type'] == Token_type.MultiplyOp:
        # To check at TokenMultpOp
        multiop_output = MultpOp(j)
        j = multiop_output["index"]
        # To check at TokenFactor
        factor_output = Factor(j)
        j = factor_output["index"]
        # To check at TokenMultOpTerm
        multiopterm_output = MultOpTerm(j)
        j = multiopterm_output["index"]
        output["node"] = Tree("MultOpTerm", [multiop_output["node"], factor_output["node"],
                                             multiopterm_output["node"]])
        output["index"] = j
        return output
    else:
        output["node"] = Tree("epsilon", [])
        output["index"] = j
        return output


def Factor(j):
    output = dict()
    Temp1 = Tokens[j].to_dict()
    if Temp1['token_type'] == Token_type.Identifier:
        # To check at Identifier
        Identifier_output = Match(Token_type.Identifier, j)
        j = Identifier_output["index"]
        output["node"] = Tree("Factor", [Identifier_output["node"]])
        output["index"] = j
        return output

    elif Temp1['token_type'] == Token_type.Number:
        # To check at Number
        Number_output = Match(Token_type.Number, j)
        j = Number_output["index"]
        output["node"] = Tree("Factor", [Number_output["node"]])
        output["index"] = j
        return output

    elif Temp1['token_type'] == Token_type.LParenthesis:
        # To check at Parenthesis
        Parenthesis_output = Parenthesis(j)
        j = Parenthesis_output["index"]
        output["node"] = Tree("Factor", [Parenthesis_output["node"]])
        output["index"] = j
        return output

    else:
        output["node"] = Tree("error", [])
        output["index"] = j
        return output


def Parenthesis(j):
    output = dict()
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.LParenthesis:
        # To check at left parenthesis
        lparenthesis_output = Match(Token_type.LParenthesis, j)
        j = lparenthesis_output["index"]
        # To check atExpression
        expression_output = Expression(j)
        j = expression_output["index"]
        # To check at right parenthesis
        rparenthesis_output = Match(Token_type.RParenthesis, j)
        j = rparenthesis_output["index"]
        output["node"] = Tree("Parenthesis", [lparenthesis_output["node"],
                                expression_output["node"], rparenthesis_output["node"]])
        output["index"] = j
        return output

    else:
        output["node"] = Tree("error", [])
        output["index"] = j
        return output


def RelOp(j):
    output = dict()
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.GreaterThanOp:
        # To check at GreaterThanOp
        GreaterThanOp_output = Match(Token_type.GreaterThanOp, j)
        j = GreaterThanOp_output["index"]
        output["node"] = Tree("RelOp", [GreaterThanOp_output["node"]])
        output["index"] = j
        return output

    elif Temp['token_type'] == Token_type.GreaterThanOrEqualOp:
        # To check at GreaterThanOrEqualOp
        GreaterThanOrEqualOp_output = Match(Token_type.GreaterThanOrEqualOp, j)
        j = GreaterThanOrEqualOp_output["index"]
        output["node"] = Tree("RelOp", [GreaterThanOrEqualOp_output["node"]])
        output["index"] = j
        return output

    elif Temp['token_type'] == Token_type.EqualEqualOp:
        # To check at EqualEqualOp
        EqualEqualOp_output = Match(Token_type.EqualEqualOp, j)
        j = EqualEqualOp_output["index"]
        output["node"] = Tree("RelOp", [EqualEqualOp_output["node"]])
        output["index"] = j
        return output

    elif Temp['token_type'] == Token_type.LessThanOrEqualOp:
        # To check at LessThanOrEqualOp
        LessThanOrEqualOp_output = Match(Token_type.LessThanOrEqualOp, j)
        j = LessThanOrEqualOp_output["index"]
        output["node"] = Tree("RelOp", [LessThanOrEqualOp_output["node"]])
        output["index"] = j
        return output

    elif Temp['token_type'] == Token_type.LessThanOp:
        # To check at LessThanOp
        LessThanOp_output = Match(Token_type.LessThanOp, j)
        j = LessThanOp_output["index"]
        output["node"] = Tree("RelOp", [LessThanOp_output["node"]])
        output["index"] = j
        return output

    elif Temp['token_type'] == Token_type.NotEqualOp:
        # To check at NotEqualOp
        NotEqualOp_output = Match(Token_type.NotEqualOp, j)
        j = NotEqualOp_output["index"]
        output["node"] = Tree("MultOpTerm", [NotEqualOp_output["node"]])
        output["index"] = j
        return output

    else:
        output["node"] = Tree("error", [])
        output["index"] = j
        return output


def AddOp(j):
    output = dict()
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.PlusOp:
        # To check at PlusOp
        PlusOp_output = Match(Token_type.PlusOp, j)
        j = PlusOp_output["index"]
        output["node"] = Tree("AddOp", [PlusOp_output["node"]])
        output["index"] = j
        return output

    elif Temp['token_type'] == Token_type.MinusOp:
        # To check at EqualOp
        MinusOp_output = Match(Token_type.MinusOp, j)
        j = MinusOp_output["index"]
        output["node"] = Tree("MultOpTerm", [MinusOp_output["node"]])
        output["index"] = j
        return output

    else:
        output["node"] = Tree("error", [])
        output["index"] = j
        return output


def MultpOp(j):
    output = dict()
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.MultiplyOp:
        # To check at MultiyOP
        MultiyOp_output = Match(Token_type.MultiplyOp, j)
        j = MultiyOp_output["index"]
        output["node"] = Tree("AddOp", [MultiyOp_output["node"]])
        output["index"] = j
        return output

    elif Temp['token_type'] == Token_type.DivideOp:
        # To check at DivideOp
        DivideOp_output = Match(Token_type.MinusOp, j)
        j = DivideOp_output["index"]
        output["node"] = Tree("MultOpTerm", [DivideOp_output["node"]])
        output["index"] = j
        return output

    else:
        output["node"] = Tree("error", [])
        output["index"] = j
        return output


def ElseClause(j):
    output = dict()
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.Else:
        # To check at Else
        Else_output = Match(Token_type.Else, j)
        j = Else_output["index"]
        # To check at statements
        statements_output = Statements(j)
        j = statements_output["index"]
        # To check at End
        end_output = Match(Token_type.end, j)
        j = end_output["index"]
        # To check at if
        if_output = Match(Token_type.If, j)
        j = if_output["index"]
        output["node"] = Tree("ElseClause", [Else_output["node"]
            , statements_output["node"], end_output["node"], if_output["node"]])
        output["index"] = j
        return output

    elif Temp['token_type'] == Token_type.end:
        # To check at End
        end_output = Match(Token_type.end, j)
        j = end_output["index"]
        # To check at if
        if_output = Match(Token_type.If, j)
        j = if_output["index"]
        output["node"] = Tree("ElseClause", [end_output["node"], if_output["node"]])
        output["index"] = j
        return output

    else:
        output["node"] = Tree("epsilon", [])
        output["index"] = j
        return output


def Stop(j):
    output = dict()
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.Identifier:
        # To check at Identifier
        id_output = Match(Token_type.Identifier, j)
        j = id_output["index"]
        output["node"] = Tree("Stop", [id_output["node"]])
        output["index"] = j
        return output

    elif Temp['token_type'] == Token_type.Number:
        # To check at number
        number_output = Match(Token_type.Number, j)
        j = number_output["index"]
        output["node"] = Tree("Stop", [number_output["node"]])
        output["index"] = j
        return output

    else:
        output["node"] = Tree("error", [])
        output["index"] = j
        return output


def Step(j):
    output = dict()
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.comma:
        comma2_output = Match(Token_type.comma, j)
        j = comma2_output["index"]
        # To check at Number
        number_output = Match(Token_type.Number, j)
        j = number_output["index"]
        output["node"] = Tree("Step", [comma2_output["node"],number_output["node"]])
        output["index"] = j
        return output

    else:
        output["node"] = Tree("epsilon", [])
        output["index"] = j
        return output


def Footer(j):
    output = dict()
    # To check at Token end
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.end:
        end_output = Match(Token_type.end, j)
        j = end_output["index"]

        # To check at Token program
        program_output = Match(Token_type.program, j)
        j = program_output["index"]

        # To check at Token Identifier
        identifier_output = Match(Token_type.Identifier, j)
        j = identifier_output["index"]

        output["node"] = Tree("Footer", [end_output["node"], program_output["node"], identifier_output["node"]])
        output["index"] = j
        return output

    else:
        output["node"] = Tree("error", [])
        output["index"] = j
    return output


def Match(a, j):
    output = dict()
    if j < len(Tokens):
        Temp = Tokens[j].to_dict()
        if Temp['token_type'] == a:
            j += 1
            output["node"] = [Temp['Lex']]
            output["index"] = j
            return output

        else:
            output["node"] = ["error"]
            output["index"] = j + 1
            errors.append("Syntax error : " + Temp['Lex'])
            return output

    else:
        output["node"] = ["error"]
        output["index"] = j + 1
        return output


# GUI
root = tk.Tk()

canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Compiler')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)


def Scan():
    file_path = 'Test'
    file = open(file_path, 'r')
    content = file.read()

    x1 = content
    split(x1.lower())

    df = pandas.DataFrame.from_records([t.to_dict() for t in Tokens])
    # print(df)

    # to display token stream as table
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()
    # start Parsing
    Node = Parse()

    # to display errorlist
    df1 = pandas.DataFrame(errors)
    dTDa2 = tk.Toplevel()
    dTDa2.title('Error List')
    dTDaPT2 = pt.Table(dTDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
    dTDaPT2.show()
    Node.draw()
    # clear your list

    # label3 = tk.Label(root, text='Lexem ' + x1 + ' is:', font=('helvetica', 10))
    # canvas1.create_window(200, 210, window=label3)

    # label4 = tk.Label(root, text="Token_type"+x1, font=('helvetica', 10, 'bold'))
    # canvas1.create_window(200, 230, window=label4)


button1 = tk.Button(text='Scan', command=Scan, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(200, 180, window=button1)
root.mainloop()

"""### """