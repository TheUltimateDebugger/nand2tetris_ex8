"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.label_counter = 0
        self.output_stream = output_stream
        self.input_filename = ""
        self.current_function_name = ""
        self.return_counter = 0

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self.input_filename = filename

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!

        if command == "add":
            self.output_stream.write("@SP\n"
                                     "A=M-1\n"
                                     "D=M\n"
                                     "@SP\n"
                                     "M=M-1\n"
                                     "A=M-1\n"
                                     "M=D+M\n")
        if command == "sub":
            self.output_stream.write("@SP\n"
                                     "A=M-1\n"
                                     "D=M\n"
                                     "@SP\n"
                                     "M=M-1\n"
                                     "A=M-1\n"
                                     "M=M-D\n")

        if command == "neg":
            self.output_stream.write("@SP\n"
                                     "A=M-1\n"
                                     "M=-M\n")

        if command == "eq":
            self.output_stream.write("@SP\n"
                                     "A=M-1\n"
                                     "D=M\n"
                                     "@SP\n"
                                     "M=M-1\n"
                                     "A=M-1\n"
                                     "D=D-M\n"
                                     f"@TRUE{self.label_counter}\n"
                                     "D;JEQ\n"
                                     "D=-1\n"
                                     f"(TRUE{self.label_counter})\n"
                                     "@SP\n"
                                     "A=M-1\n"
                                     "M=!D\n")
            self.label_counter += 1

        if command == "gt":
            self.output_stream.write("@SP\n"
                                     "A=M-1\n"
                                     "D=M\n"
                                     "@R14\n"
                                     "M=D\n"
                                     "@SP\n"
                                     "M=M-1\n"
                                     "A=M-1\n"
                                     "D=M\n"
                                     "@R13\n"
                                     "M=D\n"
                                     f"@FIRST_POS{self.label_counter}\n"
                                     "D;JGE\n"


                                     f"(FIRST_NEG{self.label_counter})\n"
                                     "@R14\n"
                                     "D=M\n"
                                     f"@SECOND{self.label_counter}\n"
                                     "D;JLT\n"
                                     "@SP\n"
                                     "A=M-1\n"
                                     "M=0\n"
                                     f"@END{self.label_counter}\n"


                                     f"(FIRST_POS{self.label_counter})\n"
                                     "@R14\n"
                                     "D=M\n"
                                     f"@SECOND{self.label_counter}\n"
                                     "D;JGE\n"
                                     "@SP\n"
                                     "A=M-1\n"
                                     "M=-1\n"
                                     f"@END{self.label_counter}\n"

                                     f"(SECOND{self.label_counter})\n"
                                     "@R13\n"
                                     "D=M\n"
                                     "@R14\n"
                                     "D=D-M\n"
                                     f"@TRUE{self.label_counter}\n"
                                     "D;JGT\n"
                                     "@SP\n"
                                     "A=M-1\n"
                                     "M=0\n"
                                     f"@END{self.label_counter}\n"
                                     "0;JMP\n"

                                     f"(TRUE{self.label_counter})\n"
                                     "@SP\n"
                                     "A=M-1\n"
                                     "M=-1\n"

                                     f"(END{self.label_counter})\n")
            self.label_counter += 1

        if command == "lt":
            self.output_stream.write("@SP\n"
                                     "A=M-1\n"
                                     "D=M\n"
                                     "@R14\n"
                                     "M=D\n"
                                     "@SP\n"
                                     "M=M-1\n"
                                     "A=M-1\n"
                                     "D=M\n"
                                     "@R13\n"
                                     "M=D\n"
                                     f"@FIRST_POS{self.label_counter}\n"
                                     "D;JGT\n"


                                     f"(FIRST_NEG{self.label_counter})\n"
                                     "@R14\n"
                                     "D=M\n"
                                     f"@SECOND{self.label_counter}\n"
                                     "D;JLT\n"
                                     "@SP\n"
                                     "A=M-1\n"
                                     "M=-1\n"
                                     f"@END{self.label_counter}\n"


                                     f"(FIRST_POS{self.label_counter})\n"
                                     "@R14\n"
                                     "D=M\n"
                                     f"@SECOND{self.label_counter}\n"
                                     "D;JGT\n"
                                     "@SP\n"
                                     "D=M\n"
                                     "@SP\n"
                                     "A=M-1\n"
                                     "M=D\n"
                                     f"@END{self.label_counter}\n"

                                     f"(SECOND{self.label_counter})\n"
                                     "@R13\n"
                                     "D=M\n"
                                     "@R14\n"
                                     "D=D-M\n"
                                     f"@TRUE{self.label_counter}\n"
                                     "D;JLT\n"
                                     "@SP\n"
                                     "A=M-1\n"
                                     "M=0\n"
                                     f"@END{self.label_counter}\n"
                                     "0;JMP\n"

                                     f"(TRUE{self.label_counter})\n"
                                     "@SP\n"
                                     "A=M-1\n"
                                     "M=-1\n"

                                     f"(END{self.label_counter})\n")
            self.label_counter += 1

        if command == "and":
            self.output_stream.write("@SP\n"
                                     "A=M-1\n"
                                     "D=M\n"
                                     "@SP\n"
                                     "M=M-1\n"
                                     "A=M-1\n"
                                     "M=D&M\n")

        if command == "or":
            self.output_stream.write("@SP\n"
                                     "A=M-1\n"
                                     "D=M\n"
                                     "@SP\n"
                                     "M=M-1\n"
                                     "A=M-1\n"
                                     "M=D|M\n")

        if command == "not":
            self.output_stream.write("@SP\n"
                                     "A=M-1\n"
                                     "M=!M\n")
        if command == "gt":
            self.output_stream.write("@SP\n"
                                     "A=M-1\n"
                                     "D=M\n"
                                     "@R13\n"
                                     "M=D"
                                     )

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        if command == "C_POP":
            self.output_stream.write("@SP\n"
                                     "M=M-1\n"
                                     "A=M\n"
                                     "D=M\n"
                                     "@R13\n"
                                     "M=D\n")
            # no constant command
            if segment == "static":
                self.output_stream.write("@" + self.input_filename + "." + str(index) + "\n"
                                                                                        "M=D\n")
            if segment == "temp":
                self.output_stream.write(f"@R{5 + index}\n"
                                         "M=D\n")
            if segment == "pointer":
                if index == 1:
                    self.output_stream.write("@THAT\n"
                                             "M=D\n")
                elif index == 0:
                    self.output_stream.write("@THIS\n"
                                             "M=D\n")
                else:
                    self.output_stream.write("ERROR!\n")

            if segment == "local":
                self.output_stream.write("@LCL\n"
                                         "D=M\n"
                                         f"@{index}\n"
                                         "D=D+A\n"
                                         "@R14\n"
                                         "M=D\n"
                                         "@R13\n"
                                         "D=M\n"
                                         "@R14\n"
                                         "A=M\n"
                                         "M=D\n")

            if segment == "argument":
                self.output_stream.write("@ARG\n"
                                         "D=M\n"
                                         f"@{index}\n"
                                         "D=D+A\n"
                                         "@R14\n"
                                         "M=D\n"
                                         "@R13\n"
                                         "D=M\n"
                                         "@R14\n"
                                         "A=M\n"
                                         "M=D\n")
            if segment == "this":
                self.output_stream.write("@THIS\n"
                                         "D=M\n"
                                         f"@{index}\n"
                                         "D=D+A\n"
                                         "@R14\n"
                                         "M=D\n"
                                         "@R13\n"
                                         "D=M\n"
                                         "@R14\n"
                                         "A=M\n"
                                         "M=D\n")
            if segment == "that":
                self.output_stream.write("@THAT\n"
                                         "D=M\n"
                                         f"@{index}\n"
                                         "D=D+A\n"
                                         "@R14\n"
                                         "M=D\n"
                                         "@R13\n"
                                         "D=M\n"
                                         "@R14\n"
                                         "A=M\n"
                                         "M=D\n")

        if command == "C_PUSH":
            if segment == "constant":
                if index < 0:
                    if index == -16384:
                        self.output_stream.write(f"@16383\n"
                                                 "D=A\n"
                                                 "D=!D\n")
                    else:
                        self.output_stream.write(f"@{-index}\n"
                                                 "D=A\n"
                                                 "D=-D\n")
                else:
                    self.output_stream.write(f"@{index}\n"
                                             "D=A\n")
            if segment == "static":
                self.output_stream.write("@" + self.input_filename + "." + str(index) + "\n"
                                                                                        "D=M\n")
            if segment == "temp":
                self.output_stream.write(f"@R{5 + index}\n"
                                         "D=M\n")
            if segment == "pointer":
                if index == 1:
                    self.output_stream.write("@THAT\n"
                                             "D=M\n")
                elif index == 0:
                    self.output_stream.write("@THIS\n"
                                             "D=M\n")
                else:
                    self.output_stream.write("ERROR!\n")

            if segment == "local":
                self.output_stream.write("@LCL\n"
                                         "D=M\n"
                                         f"@{index}\n"
                                         "A=A+D\n"
                                         "D=M\n")
            if segment == "argument":
                self.output_stream.write("@ARG\n"
                                         "D=M\n"
                                         f"@{index}\n"
                                         "A=A+D\n"
                                         "D=M\n")
            if segment == "this":
                self.output_stream.write("@THIS\n"
                                         "D=M\n"
                                         f"@{index}\n"
                                         "A=A+D\n"
                                         "D=M\n")
            if segment == "that":
                self.output_stream.write("@THAT\n"
                                         "D=M\n"
                                         f"@{index}\n"
                                         "A=A+D\n"
                                         "D=M\n")

            self.output_stream.write("@SP\n"
                                     "A=M\n"
                                     "M=D\n"
                                     "@SP\n"
                                     "M=M+1\n")

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self.output_stream.write(f"({self.current_function_name}${label})\n")

    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self.output_stream.write(f"@{self.current_function_name}${label}\n")
        self.output_stream.write("0;JMP\n")

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self.output_stream.write("@SP\n"
                                 "M=M-1\n"
                                 "A=M\n"
                                 "D=M\n")
        self.output_stream.write(f"@{self.current_function_name}${label}\n")
        self.output_stream.write("D;JNE\n")

    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0

        self.return_counter = 0
        self.current_function_name = function_name
        # injects function name
        self.write_label("")
        # push constant 0 n_vars times
        for i in range(n_vars):
            self.write_push_pop("C_PUSH", "constant", 0)

    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code

        # push return address
        self.output_stream.write(f"@{self.current_function_name}$ret.{self.return_counter}\n")

        # push local
        self.output_stream.write("@LCL\n"
                                 "D=M\n"
                                 "@SP\n"
                                 "A=M\n"
                                 "M=D\n"
                                 "@SP\n"
                                 "M=M+1\n")
        # push args
        self.output_stream.write("@ARG\n"
                                 "D=M\n"
                                 "@SP\n"
                                 "A=M\n"
                                 "M=D\n"
                                 "@SP\n"
                                 "M=M+1\n")
        # push this
        self.output_stream.write("@THIS\n"
                                 "D=M\n"
                                 "@SP\n"
                                 "A=M\n"
                                 "M=D\n"
                                 "@SP\n"
                                 "M=M+1\n")
        # push that
        self.output_stream.write("@THAT\n"
                                 "D=M\n"
                                 "@SP\n"
                                 "A=M\n"
                                 "M=D\n"
                                 "@SP\n"
                                 "M=M+1\n")

        # ARG = SP - 5 - n_args
        self.output_stream.write("@SP\n"
                                 "D=M\n"
                                 f"@{n_args}\n"
                                 "D=D-A\n"
                                 "@5\n"
                                 "D=D-A\n"
                                 "@ARG\n"
                                 "M=D\n")

        # LCL = SP
        self.output_stream.write("@SP\n"
                                 "D=M\n"
                                 "@LCL\n"
                                 "M=D\n")

        # writes the jump
        self.output_stream.write(f"@{function_name}\n")
        self.output_stream.write("0;JMP\n")

        # writes return address:
        self.output_stream.write(f"({self.current_function_name}$ret.{self.return_counter})\n")
        self.return_counter += 1

    def c(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        pass
