import threading
import bestsellers
import new_csv
import reduced
import special_offers

def run():
    t1 = threading.Thread(target=new_csv.run())
    t2 = threading.Thread(target=bestsellers.run())

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    t1 = threading.Thread(target=reduced.run())
    t2 = threading.Thread(target=special_offers.run())

    t1.start()
    t2.start()

    t1.join()
    t2.join()

if __name__ == '__main__':
    print('\nPlease Wait...')
    run()
    print('DONE')
