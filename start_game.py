from MainApp import MainApp
from MapGeneration import MapGeneration
import sys

id_people = sys.argv[1]

if id_people == "admin":
    main = MapGeneration()
    main.start_game()
elif id_people == "user":
    main = MainApp()
    main.start_game()