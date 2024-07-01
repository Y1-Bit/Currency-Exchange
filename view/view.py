def show_user(user: dict) -> str:
    response = f"""
    <html>
    <head><title>User Profile</title></head>
    <body>
        <h1>User Profile</h1>
        <p>ID: {user['id']}</p>
        <p>Name: {user['name']}</p>
    </body>
    </html>
    """
    return response
