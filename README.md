# arm-app
Asset Register Management Application

RM-APP Documentation

PURPOSE OF THE APPLICATION:
To help users create, maintain and verify assets related information / data.

APPLICATION FEATURE SET:
    1. Create / add new assets
    2. Modify existing assets related information
    3. Delete assets
    4. Verify asset information when required
    5. View all assets
        1. View individual asset details
    6. Create an audit trail for each asset
    7. Import assets information via CSV files
    8. Display statistical graphs of register information / data
    9. Move assets between different entities
    10. Issues assets to different entities
    11. Export asset register to CSV format

DOMAIN MODELING:
Model Entities:
    Assets
    • ID: int
    • Barcode: string
    • Serial No.: string
    • Date: date and time
    • Name: string
    • Type: Integer (Foreign Key)
    • Model: Integer (Foreign Key)
    • Condition: Integer (Foreign Key)
    • Status: Integer (Foreign Key)
    • Location: Integer (Foreign Key)
    • User: Integer (Foreign Key)
    • Value: integer
    • Supplier: Integer (Foreign Key)
    • Photo: link
    • Comment: string

    Locations
    • ID: integer
    • Code: integer
    • Name: string
    • Assets: Relationship (Assets)

    People
    • ID: integer
    • Barcode: string
    • First Name: string
    • Second Name: string
    • Designation: string
    • Department: Integer (Foreign Key)
    • Phone: integer
    • Email: string
    • Location: Integer (Foreign Key)

    • Stock
    • ID: int
    • Code: string
    • Name: string
    • Type: string
    • Model: string
    • Quantity: int

    • Products (models)
    • ID: int
    • Name: string
    • Type: string
    • Model: string
    • Cost: int
    • Suppliers: string

    • Suppliers
    • ID: int
    • Code: string
    • Category: string
    • Items: string
    • Location: string
    • Phone: int
    • Email: string
    • Website: link
    • Contact Person: string

APPLICATION VIEWS:
    A. Login Page
       -Landing Page
    B. Single Entry View
    C. Full Register View
    D. Query Or Create Top Bar
       - Issue assets view
       - Move assets view - Delete is just a button
