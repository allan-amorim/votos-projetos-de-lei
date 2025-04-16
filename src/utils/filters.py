import flet as ft

input_filter_number = ft.InputFilter(
    allow="0123456789,", 
    regex_string="^[0-9,]*$"
)