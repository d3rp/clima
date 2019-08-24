from clima import c, schema

@c
class C(schema):
    name: str = 'Klimenko'  # Your first name
    surname: str = 'Ma'  # Surname
    age: int = '132'  # Age is just a number

c: C = c

@c
class Something:
    def print_name(self):
        """This command prints name"""
        print(c.name + c.surname)

    def print_age(self):
        """This here, prints my age"""
        print(c.age)


