import mysql.connector
import pandas as pd
from credentials import secrets

def connect_to_database():
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            host=secrets.get('HOST'),
            user=secrets.get('DATABASE_USER'),
            password=secrets.get('DATABASE_PASSWORD'),
            database=secrets.get('DATABASE_NAME')
        )

        if connection.is_connected():
            print('Connected to MySQL database.')
            return connection
        else:
            raise ConnectionError("Failed to connect to MySQL database.")

    except mysql.connector.Error as err:
        raise ConnectionError(f"Error: {err}")

def execute_query(connection, query):
    try:
        # Create a cursor object to execute the query
        cursor = connection.cursor()

        # Execute the query
        cursor.execute(query)

        # Fetch all rows from the result
        rows = cursor.fetchall()

        # Close the cursor
        cursor.close()

        return rows

    except mysql.connector.Error as err:
        raise Exception(f"Error executing query: {err}")

def generate_report(query_list, columns_list, filename_list):
    try:
        # Connect to the MySQL database
        connection = connect_to_database()

        for query, columns, filename in zip(query_list, columns_list, filename_list):
            # Execute the query and get the results
            result_rows = execute_query(connection, query)

            # Create a DataFrame from the query results
            df = pd.DataFrame(result_rows, columns=columns)
            print(df.head())

            # Save the DataFrame as a CSV file
            df.to_csv(f'./rawdata/{filename}.csv', index=False)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the connection when done
        if connection.is_connected():
            connection.close()
            print('Connection to MySQL database closed.')

if __name__ == "__main__":
    query1 = """SELECT
                    product_title,
                    SUM(carts_total) AS revenue
                FROM
                    carts  
                GROUP BY
                    product_id, product_title
                ORDER BY
                    revenue DESC
                LIMIT
                    20;"""

    query2 = """WITH Top20Users AS (
                SELECT
                    userid,
                    COUNT(DISTINCT id) AS post_count
                FROM
                    posts
                GROUP BY
                    userid
                ORDER BY
                    post_count DESC
                LIMIT 20
            )

            SELECT
                u.id,
                u.firstName,
                tu.post_count,
                COUNT(DISTINCT c.id) AS comment_count
            FROM
                Top20Users tu
            LEFT JOIN
                posts p ON tu.userid = p.userid
            LEFT JOIN
                comments c ON p.id = c.postid
            LEFT JOIN
                users u ON tu.userid = u.id
            GROUP BY
                tu.userid, u.firstName, tu.post_count
            ORDER BY
                tu.post_count DESC;"""

    query3 = """SELECT
                    u.addressstate AS state,
                    SUM(c.carts_discountedTotal) AS total_revenue
                FROM
                    users u
                JOIN
                    carts c ON u.id = c.carts_userid
                GROUP BY
                    u.addressstate
                ORDER BY
                    total_revenue DESC
                LIMIT 10;"""

    query_list = [query1, query2, query3]
    columns_list = [['ProductName', 'Revenue'], ['user_id', 'user_name', 'post_count', 'comment_count'],
                    ['user_state', 'total_revenue']]
    filename_list = ['q1_response', 'q2_response', 'q3_response']

    generate_report(query_list, columns_list, filename_list)
