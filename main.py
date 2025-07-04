from flask import Flask, request, jsonify
import cx_Oracle
app = Flask(__name__)

dsn_tns = cx_Oracle.makedsn('localhost', 1521, service_name='XEPDB1')
conn = cx_Oracle.connect(user='SYSTEM', password='123', dsn=dsn_tns)
cursor = conn.cursor()
@app.route('/customers')
def home():
    return jsonify(message="Oracle Flask API is running!")

@app.route('/customers', methods=['POST'])
def create_customers():
    data = request.json
    sql = """
        INSERT INTO customers (NAME, ADDRESS, MOBILENO, EMAIL, NTN_STRN_NO)
        VALUES (:1, :2, :3, :4, :5)
    """
    cursor.execute(sql, (
        data["NAME"], data["ADDRESS"], data["MOBILENO"],
        data["EMAIL"], data["NTN_STRN_NO"]
    ))
    conn.commit()
    return jsonify(message="Created successfully"), 201
@app.route('/customers', methods=['GET'])
def get_customers():
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    customers = []
    for row in rows:
        customers.append({
            "CUSTOMER_ID": row[0],
            "NAME": row[1],
            "ADDRESS": row[2],
            "MOBILENO": row[3],
            "EMAIL": row[4],
            "NTN_STRN_NO": row[5]
        })
    return jsonify(customers)
@app.route('/customers/<int:customer_id>', methods=['PUT'])

def update_customers(customer_id):
    data = request.json
    sql = """
        UPDATE customers
        SET NAME = :1, ADDRESS = :2, MOBILENO = :3,
            EMAIL = :4, NTN_STRN_NO = :5
        WHERE customer_ID = :6
    """
    cursor.execute(sql, (
        data["NAME"], data["ADDRESS"], data["MOBILENO"],
        data["EMAIL"], data["NTN_STRN_NO"], customer_id
    ))
    conn.commit()
    return jsonify(message="Updated successfully")
@app.route('/customers / <int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    cursor.execute("DELETE FROM customers WHERE customer_ID = :1", [customer_id])
    conn.commit()
    return jsonify(message="Deleted successfully")

if __name__ == '__main__':
   app.run(debug=True,port=5000)
