'''def calculate(n):
    total = 0
    for i in range(n):
        total += i
    return total

def add_strings_together(string1, string2):
    result = string1 + " " + string2
    return result

beweis = "ich bin der Beweis!"
print("Wird ausgeführt")'''

'''strimgs_zusammenfühtren = add_strings_together("Ich", "Du")
result = calculate(5)
print("Summe ist: ", result)'''


'''def find_min_number(numbers):
    min_number = numbers[0]

    for num in numbers:
        if num < min_number:
            min_number = num

    return min_number

min_number = find_min_number([2, 3, 1, 5, 4])
print(f"Die kleinste Zahl ist {min_number}")'''

'''def is_odd_number(num):          '''
'''    """ Checks if num is odd """'''
'''    if num % 2 == 0:            '''
'''        return True             '''
'''    else:                       '''
'''        return False            '''
'''                                '''
'''print(is_odd_number(4))         '''

'''def remove_special_char(username):                 '''
""" Remove special characters and space from the username """
'''  updated_username = ""                           '''
'''  for char in username:                           '''
'''    if char not in ";.@#$%ˆ&*:_ ":                '''
'''      updated_username += char                    '''
'''  return updated_username                         '''
'''                                                  '''
'''def add_at_symbol(username):                       '''
'''  """ add the @ symbol at the end of the username '''"""
'''  return username + "@"                           '''
'''                                                  '''
'''def add_domain_name(username):                     '''
  add the domain (mail.com) name to the username
'''  return username + "mail" + ".com"               '''
'''                                                  '''
'''username = "user&#123_ @"  # username we want to c'''onvert to email
'''new_username = remove_special_char(username)      '''
'''new_username_with_at = add_at_symbol(new_username)'''
'''user_email = add_domain_name(new_username_with_at)'''
'''print(user_email)  # Expected user123@mail.com    '''