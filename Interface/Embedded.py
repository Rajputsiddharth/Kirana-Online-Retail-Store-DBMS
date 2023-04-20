import mysql.connector
import maskpass
from tabulate import tabulate

# Establish connection with MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="siddharth@sem3",
  database="kirana"
)


# Create cursor object to execute SQL queries
mycursor = mydb.cursor()

###
# Function to add customer to the database
def add_customer():
  # Get input from user
  first_name = input("Enter first name: ")
  middle_name = input("Enter middle name: ")
  last_name = input("Enter last name: ")
  date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
  phone_num = input("Enter phone number: ")
  email_address = input("Enter email address: ")
  password = maskpass.askpass(prompt="Enter password: ", mask="*")
  apt_number =input("Enter apartment number: ")
  street = input("Enter street: ")
  city = input("Enter city: ")
  state = input("Enter state: ")
  pincode = int(input("Enter pincode: "))
  
  
  # Define SQL query and data values
  sql = "INSERT INTO Customer (first_name, middle_name, last_name, date_of_birth, phone_num, email_address, password, apt_number, street, city, state, pincode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
  val = (first_name, middle_name, last_name, date_of_birth, phone_num, email_address, password, apt_number, street, city, state, pincode)

  # Execute query and commit changes
  mycursor.execute(sql, val)
  mydb.commit()

  print(mycursor.rowcount, "record inserted.")

###
# Function to add seller to the database
def add_seller():
  # prompt user to input values for attributes
  name = input("Enter seller name: ")
  phone_num = input("Enter phone number: ")
  email_address = input("Enter email address: ")
  password = maskpass.askpass(prompt="Enter password: ", mask="*")
  apt_number = int(input("Enter apartment number: "))
  street = input("Enter street address: ")
  city = input("Enter city: ")
  state = input("Enter state: ")
  pincode = int(input("Enter pincode: "))

  # Define SQL query and data values
  sql = "INSERT INTO Seller (name, phone_num, email_address, password, apt_number, street, city, state, pincode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
  val = (name, phone_num, email_address, password, apt_number, street, city, state, pincode)

  # Execute query and commit changes
  mycursor.execute(sql, val)
  mydb.commit()

  print(mycursor.rowcount, "record inserted.")


def add_product():
  name = input("Enter the name of the product: ")
  price = float(input("Enter the price of the product: "))
  quantity = int(input("Enter the quantity of the product: "))
  rating = int(input("Enter the rating of the product: "))
  description = input("Enter the description of the product: ")
  seller_id = int(input("Enter the seller ID for the product: "))
  category_id = int(input("Enter the category ID for the product: "))

  # Define SQL query and data values
  sql = "INSERT INTO Product (name, price, quantity, rating, description, seller_id, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
  val = (name, price, quantity, rating, description, seller_id, category_id)

  # Execute query and commit changes
  mycursor.execute(sql, val)
  mydb.commit()

  print(mycursor.rowcount, "record inserted.")


###
# Function to login as customer
def login_customer():
  email_address = input("Enter Email Address: ")
  password = maskpass.askpass(prompt="Password:", mask="*")
  # Embedded SQL query to verify customer login details
  sql = "SELECT * FROM Customer WHERE email_address = %s AND password = %s"
  values = (email_address, password)
  # Executing the SQL query using cursor.execute() method
  mycursor.execute(sql, values)
  # Fetching the result
  result = mycursor.fetchall()
  # Checking if the result is empty
  # Checking if the login details are correct
  if result is None:
      return False
  else:
      return result[0][0] 

###
# Function to login as a admin
def login_admin():
  username = input("Enter Username: ")
  password = maskpass.askpass(prompt="Password:", mask="*")
  # Embedded SQL query to verify admin login details
  sql = "SELECT * FROM Admin WHERE username = %s AND password = %s"
  values = (username, password)
  # Executing the SQL query using cursor.execute() method
  mycursor.execute(sql, values)
  # Fetching the result
  result = mycursor.fetchall()
  # Checking if the result is empty
  # Checking if the login details are correct
  if len(result) == 0:
    return False
  else:
    return True

### 
# Function to login as seller
def login_seller():
  phone_num = input("Enter Email Address: ")
  password = maskpass.askpass(prompt="Password:", mask="*")
  # Embedded SQL query to verify seller login details
  sql = "SELECT * FROM Seller WHERE email_address = %s AND password = %s"
  values = (phone_num, password)
  # Executing the SQL query using cursor.execute() method
  mycursor.execute(sql, values)
  # Fetching the result
  result = mycursor.fetchall()
  # Checking if the result is empty
  # Checking if the login details are correct
  if len(result) == 0:
    return False
  else:
    return True
  
def add_to_cart(customer_id):
  # Get input from user
  product_id = int(input("Enter product ID: "))
  quantity = int(input("Enter quantity: "))

  # Check if the product exists
  mycursor = mydb.cursor()
  mycursor.execute("SELECT * FROM Product WHERE product_id = %s", (product_id,))
  product = mycursor.fetchone()
  if product:
    # Confirm with the customer if they want to add the product to their cart
    confirm = input("Do you want to add " + product[1] + " to your cart? (y/n): ")
    if confirm.lower() == 'y':
      # Add the product to the customer's shopping cart
      mycursor.execute("INSERT INTO ShoppingCart (total_cost, taxes, customer_id, product_id, quantity) VALUES (%s, %s, %s, %s, %s)", (product[2], product[3], customer_id, product_id, quantity))
      mydb.commit()
      print("Product added to cart successfully!")
    else:
      print("Product not added to cart.")
  else:
    print("Product not found.")

def view_cart(customer_id):
    cursor = mydb.cursor()
    cursor.execute("SELECT p.product_id, p.name, p.price, s.name AS seller_name, s.phone_num AS seller_phone_num, s.email_address AS seller_email, c.quantity FROM Product p JOIN ShoppingCart c ON p.product_id = c.product_id JOIN Seller s ON p.seller_id = s.seller_id WHERE c.customer_id = %s", (customer_id,))
    result = cursor.fetchall()
    if len(result) == 0:
        print("Your cart is empty.")
    else:
        print("Your cart:")
        for row in result:
            print(f"Product ID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Price: {row[2]}")
            print(f"Quantity: {row[6]}")
            print("-----")


###
# Function to display all customers in the database
def view_customers():
  mycursor.execute("SELECT * FROM customer")

  results = mycursor.fetchall()

  # Printing the customer details
  print("CUSTOMERS")
  print("----------")
  for row in results:
    print("Customer ID:", row[0])
    print("Name:", row[1])
    print("Phone Number:", row[2])
    print("Email Address:", row[3])
    print("Apartment Number:", row[4])
    print("Street:", row[5])
    print("City:", row[6])
    print("State:", row[7])
    print("Pincode:", row[8])
    print("----------")

  # for row in results:
  #   print(row)

###
# Function to display all sellers in the database
def view_sellers():
  mycursor.execute("SELECT * FROM seller")

  results = mycursor.fetchall()

  for seller in results:
      print("Seller ID:", seller[0])
      print("Name:", seller[1])
      print("Phone Number:", seller[2])
      print("Apartment Number:", seller[3])
      print("Street:", seller[4])
      print("City:", seller[5])
      print("State:", seller[6])
      print("Pincode:", seller[7])
      print("----------")

###
def view_categories():
    mycursor.execute("SELECT * FROM category")
    results = mycursor.fetchall()
    
    headers = ["Category ID", "Name"]
    table = tabulate(results, headers=headers, tablefmt="grid")
    print(table)

###
# Function to display all products in the database
def view_products():
    mycursor.execute("SELECT * FROM product")
    results = mycursor.fetchall()
    for row in results:
        print("Product ID:", row[0])
        print("Name:", row[1])
        print("Price:", row[2])
        print("Quantity:", row[3])
        print("Rating", row[4])
        print("Description", row[5])
        print("Seller ID", row[6])
        print("Category ID", row[7])
        print("----------")
        
###
# function for OLAP query 1
def olap_query_1():
    # execute query
    mycursor.execute("""
        SELECT YEAR(order_date) AS year,
               MONTH(order_date) AS month,
               category.name AS category_name,
               SUM(purchased.quantity) AS quantity
        FROM Orders
        JOIN Purchased ON Orders.order_id = Purchased.order_id
        JOIN Product ON Purchased.product_id = Product.product_id
        JOIN category ON Product.category_id = category.category_id
        GROUP BY year, month, category_name WITH ROLLUP;
    """)
    # fetch and print results
    results = mycursor.fetchall()
    headers = ["Year", "Month", "Category Name", "Quantity"]
    table = tabulate(results, headers=headers, tablefmt="grid")
    print(table)

###
# function for OLAP query 2
def olap_query_2():
    # execute query
    mycursor.execute("""
        SELECT Seller.name, Category.name, SUM(Product.price * Purchased.quantity) as revenue
        FROM Seller
        INNER JOIN Product ON Seller.seller_id = Product.seller_id
        INNER JOIN Category ON Product.category_id = Category.category_id
        INNER JOIN Purchased ON Product.product_id = Purchased.product_id
        GROUP BY Seller.name, Category.name;
    """)
    # fetch and print results
    results = mycursor.fetchall()
    headers = ["Seller Name", "Category Name", "Revenue"]
    table = tabulate(results, headers=headers, tablefmt="grid")
    print(table)

###
# function for OLAP query 3
# function for OLAP query 3
def olap_query_3():
    # execute query
    mycursor.execute("""
        SELECT 
            CASE 
                WHEN YEAR(date_of_birth) >= 2003 THEN 'Under 18'
                WHEN YEAR(date_of_birth) BETWEEN 1994 AND 2002 THEN '18-27'
                WHEN YEAR(date_of_birth) BETWEEN 1984 AND 1993 THEN '28-37'
                WHEN YEAR(date_of_birth) BETWEEN 1974 AND 1983 THEN '38-47'
                ELSE 'Over 47'
            END AS age_range, city, COUNT(*) AS num_customers
        FROM kirana.Customer
        GROUP BY age_range, city
        ORDER BY age_range ASC, num_customers DESC;
    """)
    # fetch and print results
    results = mycursor.fetchall()
    headers = ["Age Range", "City", "Number of Customers"]
    print(tabulate(results, headers=headers,tablefmt="grid"))

###
# function for OLAP query 4
def olap_query_4():
    # execute query
    mycursor.execute("""
        SELECT s.name AS 'Seller', 
               COUNT(CASE WHEN p.rating = 1 THEN 1 END) AS '1 Star', 
               COUNT(CASE WHEN p.rating = 2 THEN 1 END) AS '2 Stars', 
               COUNT(CASE WHEN p.rating = 3 THEN 1 END) AS '3 Stars', 
               COUNT(CASE WHEN p.rating = 4 THEN 1 END) AS '4 Stars', 
               COUNT(CASE WHEN p.rating = 5 THEN 1 END) AS '5 Stars'
        FROM Seller s
        JOIN Product p ON s.seller_id = p.seller_id
        JOIN Purchased pu ON p.product_id = pu.product_id
        GROUP BY s.seller_id;
    """)
    # fetch and print results
    results = mycursor.fetchall()
    headers = ['Seller', '1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars']
    rows = [list(row) for row in results]
    print(tabulate(rows, headers=headers, tablefmt="grid"))

### 
# function for OLAP query 5
def olap_query_5():
    # execute query
    mycursor.execute("""
        SELECT Customer.first_name, COUNT(Orders.order_id) AS Total_Orders
        FROM Customer
        INNER JOIN Orders ON Customer.customer_id = Orders.customer_id
        GROUP BY Customer.customer_id
        ORDER BY Total_Orders DESC
        LIMIT 10;
    """)
    # fetch results
    results = mycursor.fetchall()
    
    # print results
    print("Top 10 customers who have made the most number of orders:")
    print(tabulate(results, headers=['Customer Name', 'Total Orders'], tablefmt="grid"))

###
# function for OLAP query 6
def olap_query_6():
    # execute query
    mycursor.execute("""
        SELECT COUNT(*) AS num_customers, YEAR(date_of_birth) AS birth_year, MONTH(date_of_birth) AS birth_month
        FROM Customer
        GROUP BY birth_year, birth_month
    """)

    # print results
    results = mycursor.fetchall()
    headers = ["Number of Customers", "Birth Year", "Birth Month"]
    print(tabulate(results, headers=headers, tablefmt="grid"))


def search_product(product_name):
    # Execute the SQL query to select the product by name
    query = "SELECT * FROM Product WHERE name = %s"
    mycursor.execute(query, (product_name,))

    # Fetch the results of the query
    product = mycursor.fetchone()

    # Display the details of the product
    if product is not None:
        print("################\nProduct ID:", product[0])
        print("Name:", product[1])
        print("Price:", product[2])
        print("Quantity:", product[3])
        print("Rating:", product[4])
        print("Description:", product[5])
        print("################")
    else:
        print("Product not found.")

###
# Main Function
while (True):
  print("******************************\nWelcome to Kirana, One stop destination for all your needs ;)\n1) Login\n2) Sign Up\n3) Enter as Admin\n4) Exit\n******************************")
  choice = int(input("Enter your choice: "))

  # Login 
  if choice == 1:
    while True:
      print("******************************\n1) Login as Customer\n2) Login as Seller\n3) Go Back\n******************************")
      i1 = int(input("Enter your choice: "))
      if i1 == 1:
        result=login_customer()
        if result:
          print("Login Successful! ")
          while True:
            # print("1) View Categories\n2) View Products\n3) View Cart\n4) Add to Cart\n5) Remove from Cart\n6) Checkout\n7) Logout")
            print("1) View Categories\n2) View Products\n3) Search Product\n4)Add to Cart \n5) View Cart\n6) Logout")
            i2 = int(input("Enter your choice: "))
            if i2 == 1:
              view_categories()
            elif i2 == 2:
              view_products()
            elif i2 == 3:
              product_name = input("Enter product name: ")
              search_product(product_name)
            elif i2 == 4:
              add_to_cart(result)
            elif i2 == 5:
              view_cart(result)
            elif i2 == 6:
              break
            
            # elif choice == 3:
            #   #view_cart()
            # elif choice == 4:
            #   #add_to_cart()
            # elif choice == 5:
            #   #remove_from_cart()
            # elif choice == 6:
            #   #checkout()
            # elif choice == 7:
            #   break
        else:
          print("OOOPS, Login Failed!")
      elif i1 == 2: 
        if login_seller():
          print("Login Successful!")
          while True:
            print("1) View Categories\n2) View Products\n3) View Analytics\n4) Add Product\n5) Logout")
            i2 = int(input("Enter your choice: "))
            if i2 == 1:
              view_categories()
            elif i2 == 2:
              view_products()
            elif i2 == 3:
              # olap_query_1()
              # olap_query_2()
              # olap_query_3()
              olap_query_4()
              # olap_query_5()
              # olap_query_6()
            elif i2 == 4:
              add_product()
            elif i2 == 5:
              break
        else:
          print("OOOPS, Login Failed!")
      elif i1 == 3:
        break


  # Sign Up
  elif choice == 2:
    while True:
      print("******************************\n1) Sign Up as Customer\n2) Sign Up as Seller\n3) Go Back\n******************************")
      i1 = int(input("Enter your choice: "))
      if i1 == 1:
        add_customer()
        print("Thank you for signing up!")
      elif i1 == 2:
        add_seller()
        print("Thank you for signing up!")
      elif i1 == 3:
        break
  
  # Admin Login
  elif choice == 3:
    if login_admin():
      print("Login Successful!")
      while True:
        print("******************************\n1) View Customers\n2) View Sellers\n3) View Categories\n4) View Products\n5) View Analytics\n6) Add Product\n7) Logout\n******************************")
        i1 = int(input("Enter your choice: "))
        if i1 == 1:
          view_customers()
        elif i1 == 2:
          view_sellers()
        elif i1 == 3:
          view_categories()
        elif i1 == 4:
          view_products()
        elif i1 == 5:
          while True:
            print("******************************\n1) OLAP Query 1\n2) OLAP Query 2\n3) OLAP Query 3\n4) OLAP Query 4\n5) OLAP Query 5\n6) OLAP Query 6\n7) Go Back\n******************************")
            i2 = int(input("Enter your choice: "))
            if i2 == 1:
              olap_query_1()
            elif i2 == 2:
              olap_query_2()
            elif i2 == 3:
              olap_query_3()
            elif i2 == 4:
              olap_query_4()
            elif i2 == 5:
              olap_query_5()
            elif i2 == 6:
              olap_query_6()
            elif i2 == 7:
              break
        elif i1 == 6:
          add_product()
        elif i1 == 7:
          break
    else:
      print("OOOPS, Login Failed!")
  
  # Exit the application
  elif choice == 4:
    print("Thank you for using Kirana! Come back soon, we know you can't resist us ;)")
    break

