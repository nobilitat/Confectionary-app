def get_units(connect):
    """Получение единиц измерения"""

    cursor = connect.cursor()
    cursor.execute("""
        select unit_name from unit
    """)
    result = cursor.fetchall()
    cursor.close()
    return result
