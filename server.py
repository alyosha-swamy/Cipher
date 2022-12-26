import socket
import sqlite3
import curses
conn = sqlite3.connect(':memory:')
conn.execute('''
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    ip_address TEXT
);
''')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(5)

stdscr = curses.initscr()

while True:
    client_socket, address = server_socket.accept()
    ip_address = address[0]
    username = client_socket.recv(1024).decode('utf-8')
    conn.execute('''
    INSERT INTO users (username, ip_address)
    VALUES (?, ?)
    ''', (username, ip_address))
    conn.commit()
    stdscr.addstr(f'{username} is now online\n')
    stdscr.refresh()
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        if not message:
            break
        stdscr.addstr(f'{username}: {message}\n')
        stdscr.refresh()
    client_socket.close()
    conn.execute('''
    DELETE FROM users
    WHERE username = ?
    ''', (username,))
    conn.commit()
    stdscr.addstr(f'{username} is now offline\n')
    stdscr.refresh()

curses.endwin()
server_socket.close()
