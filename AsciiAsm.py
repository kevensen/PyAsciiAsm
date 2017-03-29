#!/usr/bin/python

import argparse
import sys

class Command:

    def __init__(self, command):
        self.command = command

    def get_chars(self):
        return list(self.command)

    def pad(self, ascii_list):
        try:
            # Test if last value is an int
            int(ascii_list[len(ascii_list) - 1])
            ascii_list.append(0)
            while len(ascii_list) % 4 > 0:
                ascii_list.append(0)
        except ValueError:
            ascii_list.append('00')
            while len(ascii_list) % 4 > 0:
                ascii_list.append('00')
        return ascii_list

    def get_ascii_base10(self):
        ascii_list = []
        for i in range(0, len(self.get_chars())):
            ascii_list.append(ord(self.get_chars()[i]))
        return self.pad(ascii_list)

    def get_ascii_base16(self):
        ascii_list = []
        for i in range(0, len(self.get_chars())):
            ascii_list.append(format(ord(self.get_chars()[i]),'x'))
        return self.pad(ascii_list)

    def group_by_double_word(self):
        n = 4
        return [self.get_ascii_base16()[i:i+n]
                for i in range(0, len(self.get_ascii_base16()), n)]

    def group_by_double_word_reverse(self):
        return self.group_by_double_word()[::-1]

    def group_by_double_word_reverse_pretty(self):
        double_words_pretty = []
        for i in range(0,len(self.group_by_double_word_reverse())):
            double_words_pretty.append('0x' + ''.join(
                                        self.group_by_double_word_reverse()[i]))
        return double_words_pretty

    def get_asm(self):
        for i in range(0, len(self.group_by_double_word_reverse_pretty())):
            sys.stdout.write('push ' +
                            self.group_by_double_word_reverse_pretty()[i] +"\n")

    def get_raw(self):
        push_eax_op_code = '50'
        bytes_list = []
        for i in range(0,len(self.group_by_double_word_reverse())):
            bytes_list.append(push_eax_op_code)
            for j in range(0, len(self.group_by_double_word_reverse()[i])):
                bytes_list.append(self.group_by_double_word_reverse()[i][j])

        return bytes_list




def main():
    parser = argparse.ArgumentParser(description='Convert a command string ' +
                                    'to ASCII characters that can be pushed ' +
                                    'on a stack with assembly.')
    parser.add_argument('--command',help='The string to convert',required=True)
    output_group = parser.add_mutually_exclusive_group(required=True)
    output_group.add_argument('--asm',
                       help='Output as a set of x86 ASM instructions.',
                       dest='asm', action='store_true')
    output_group.add_argument('--raw',
                       help='Output as a group of x86 bytes as a single string.',
                       dest='raw', action='store_true')

    parser.set_defaults(asm=False)
    parser.set_defaults(raw=False)

    args = parser.parse_args()
    my_command = Command(args.command)

    if args.asm:
        my_command.get_asm()
    elif args.raw:
        sys.stdout.write(''.join(my_command.get_raw())+'\n')

if __name__ == "__main__":
    main()
