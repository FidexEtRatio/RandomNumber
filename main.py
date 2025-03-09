from nasa_source import get_current_sun_data
from entropy import get_entropy
from local_source import get_images, cleanup

#def generate():
#    num = 0
#
#def exit():
#    cleanup()
#
#def main():
#    print("Random number generator")
#    run = True
#    while run:
#        print("Choose an option:\n")
#        print("1. Generate random number\n")
#        print("2. Exit\n")
#        choice = input("Enter choice: ")
#        choice = int(choice)
#        if choice == 1:
#            generate()
#        elif choice == 2:
#            exit()
#            run = False
#
#
#
#if __name__ == "__main__":
#    main()

#get_current_sun_data()
#img_list_test = get_images()
#print("Images found: ", img_list_test)
#cleanup()
#entropy = get_entropy("./images/20250309_025609_4096_211193171n.jpg")
#print(entropy)

# test entropies:
# HMI171 = 6.5415983
# 211193171n = 6.701223
# 0094 = 6.7808456
# 0131 = 5.93037
# HMIBC = 4.6175113
# 0171 = 6.8162866