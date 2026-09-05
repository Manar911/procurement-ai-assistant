PROCUREMENT_SCHEMA = """
MongoDB database: procurement_assistant
Collection: purchase_orders

Important fields:

creation_date:
- MongoDB Date
- The date the order was created in the system.
- Use this field for questions about when orders were created.

purchase_date:
- MongoDB Date or null
- User-entered purchase date.
- May be backdated.

fiscal_year:
- String
- Example: "2013-2014"
- California fiscal year runs from July 1 to June 30.

purchase_order_number:
- String
- Purchase order numbers are not globally unique.

department_name:
- String
- Name of the purchasing department.

supplier_name:
- String
- Name of the supplier.

acquisition_type:
- String
- Examples include:
  NON-IT Goods
  NON-IT Services
  IT Goods
  IT Services

acquisition_method:
- String
- Procurement acquisition method.

item_name:
- String
- Name of the purchased item.

item_description:
- String or null
- Description of the purchased item.

quantity:
- Numeric
- Quantity purchased.

unit_price:
- Numeric or null
- Price per unit.

total_price:
- Numeric or null
- Total line price.
- Does not include taxes or shipping.

IMPORTANT BUSINESS RULES:

1. A MongoDB document represents a procurement line record,
   not necessarily one complete purchase order.

2. For counting unique purchase orders, use the combination:
   department_name + purchase_order_number.

3. Use creation_date for questions about orders being created.

4. Never modify database records.

5. The database must only be queried using read-only operations.
"""