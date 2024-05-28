from regex import DataTypeChecker

#Test for regex expressions. Provided with value, expected result and regular expression to apply
def run_tests():
    checker = DataTypeChecker()

    def test(value, expected, func):
        result = func(value)
        
        if result == expected:
            print(f"PASS: {value} - {result}")
        else:
            print(f"FAIL: {value} - {result}")

    #Test cases for check_email_address
    print("\nTesting check_email_address:")
    test("example@example.com", True, checker.check_email_address)
    test("user.name+tag+sorting@example.com", True, checker.check_email_address)
    test("user@sub.example.co.uk", True, checker.check_email_address)
    test("user@example.web", True, checker.check_email_address)
    test("plainaddress", False, checker.check_email_address)
    test("example.com", False, checker.check_email_address)
    test("@example.com", False, checker.check_email_address)
    test("user@", False, checker.check_email_address)
    test("", False, checker.check_email_address)
    test(None, False, checker.check_email_address)

    #Test cases for check_date
    print("Testing check_date:")
    test("2024-05-23", True, checker.check_date)
    test("05/23/2024", True, checker.check_date)
    test("2024.05.23", True, checker.check_date)
    test("2024/05/23", True, checker.check_date)
    test("23-05-2024", False, checker.check_date)
    test("not a date", False, checker.check_date)
    test("", False, checker.check_date)
    test("20240523", False, checker.check_date)
    test(None, False, checker.check_date)

    #Test cases for check_telephone_number
    print("\nTesting check_telephone_number:")
    test("+1-800-555-5555", True, checker.check_telephone_number)
    test("8005555555", True, checker.check_telephone_number)
    test("(800) 555-5555", True, checker.check_telephone_number)
    test("+44 20 7946 0958", True, checker.check_telephone_number)
    test("123", False, checker.check_telephone_number)
    test("phone number", False, checker.check_telephone_number)
    test("800-555-555", False, checker.check_telephone_number)
    test("", False, checker.check_telephone_number)
    test(None, False, checker.check_telephone_number)


    #Test cases for check_url
    print("\nTesting check_url:")
    test("https://www.example.com", True, checker.check_url)
    test("http://example.com", True, checker.check_url)
    test("www.example.com", True, checker.check_url)
    test("example.com", True, checker.check_url)
    test("http://example.com/path?color=purple", True, checker.check_url)
    test("example", False, checker.check_url)
    test("http://", False, checker.check_url)
    test("://example.com", False, checker.check_url)
    test("", False, checker.check_url)
    test(None, False, checker.check_url)

    #Test cases for check_price
    print("\nTesting check_price:")
    test("$100", True, checker.check_price)
    test("€100.50", True, checker.check_price)
    test("$100.123", True, checker.check_price)
    test("100", True, checker.check_price)
    test("€100", True, checker.check_price)
    test("100.", False, checker.check_price)
    test("one hundred", False, checker.check_price)
    test("100.1234", False, checker.check_price)
    test("", False, checker.check_price)
    test(None, False, checker.check_price)

run_tests()
