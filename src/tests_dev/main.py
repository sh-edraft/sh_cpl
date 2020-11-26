from tests_dev.program import Program

if __name__ == '__main__':
    program = Program()
    program.create_configuration()
    program.create_services()
    program.main()
