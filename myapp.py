#Παιχίδι Ναυμαχία

#Bobus έκδοση την λέω πειραματρική

#Δεν χρειάζονται τα παρακάτω,διότι δεν θα διορθώσουν,συμφοιτητές μας

#1.Βασικό πααιχνίδι (καλά είναι να μην τρέχεται την βασική έκδοση και συχρόνως την πειραματική.
#2.Bonus Οταν θέλετε,να παίξετε,από τον ίδιο υπολογιστή,πρέπει να ανοίξετε σελίδα και να πατήσετε
# Ctrl+Αριστερό Shift+Ν,για να μπείτε You've Igognito και αφήστε τσεκαρισμένα
#Block third party cookies για να δουλέψετε το Gianni και τη Maria,διαφορετικά θα γίνιυν μετά από λίγο το ίδιο πρόσωπο
#Για τον δεύτερο παίχτη κάντε εισαγωγή με http://127.0.0.1:5000/logme
#Οι τιμές που δίνει ο παίχτης,με print τα εκτυπώνω στην  consola , Thonny για να τις βλέπουμε κιόλας.
#Πρέπει οποσδήποτε να δίνεται ακέραιες τιμές,το παιχνίδι για x>7 και ότι y να βάλετε ξεκινά,
#Aλλά πάντα ακέραιες τιμές,αν δωστε x,y έξω,από τα,όρια της σχάρας sernse ,σας ζητά,πάλι να ξαναδώσεται τιμή μέσα
#στα όρια.



# Εισάγουμε το framework flask
from flask import Flask,render_template,request,session,g,url_for,redirect   # Εισάγουμε τη βιβλιοθήκη flask
import random # Εισάγουμε τη βιβλιοθήκη random της python
# Εισάγουμε τη βιβλιοθήκη sense_emu (ή sense_hat)
from sense_emu import SenseHat

s=SenseHat()

# Με την clear() σβήνουμε τυχόν παλιές τιμές
# που έχει δεχθεί η LED συστοιχία
s.clear()

# Επιλογή χρωμάρων και δημιουργια της λίστας shipmap
green=[0,200,0] # Πλοία_ια τις θέσεις των στόχων χρησιμοποιούμε το πράσινο χρώμα,
black=[0,0,0]   # ενώ κανένα χρώμα για τις υπόλοιπες θέσεις.
blue=[0,0,200]  # Βασική έκδοση Για τις θέσεις των βομβών χρησιμοποιούμε μπλέ χρώμα
red=[200,0,0]
light_blue=[0,200,200] #χρώμα όταν χτυπά πράσινο πλοίο του ΜΠΛΕ πάιχτης
yellow=[200,200,0] #χρώμα όταν χτυπά πράσινο πλοίο του ΚΟΚΚΙΝΟΣ πάιχτης
black=[0,0,0]

# Δημιουργούμε τη λίστας μεγέθους 64 στοιχείων
# που περιλαμβάνουν 10 θέσεις-στόχους:
shipmap=[
(0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0),
(0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0),
(0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0),
(0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0),
(0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0),
(0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0),
(0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0),
(0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0),
]

# Δημιουργούμε μια λίστα που περιέχει μικρότερες
# λίστες με τα στοιχεία του κάθε χρήστη.
# Αρχικοποιούμε τη λίστα users:
users= []
# Με την append() προσθέτουμε κάθε χρήστη ως
# μια μικρότερη λίστα αποτελούμενη από τρία πεδία.
# Το πρώτο πεδίο αφορά ένα μοναδικό αριθμό (user id).
# Το δεύτερο πεδίο αφορά το όνομα του χρήστη (username).
# Τέλος, το τρίτο αφορά τον κωδικό του χρήστη (password)
users.append([1, 'Giannis','kodikos_Gianni'])
users.append([2, 'Maria','kodikos_Marias'])


#Δίνουμε το όνομα app στο flask
app = Flask(__name__)
app.secret_key = "Μυστικό_Κλειδί_Κρυπτογράφησης"


##########before_request#########
@app.before_request
def before_request():
    # Αρχικοποιούμε το αντικείμενο g.user:
    g.user=None
    #αρχικοποίηση μεταβλητων,για να αλλάζουν τα μυνήματα στην html σελίδες
    g.color=None
    g.comment=None
    g.point=None

# Ελέγχουμε αν είναι κατειλημμένο το session cookie,
    # αν δηλαδή έχει συνδεθεί ο χρήστης.
    if 'user_id' in session:
        # Διατρέχουμε τη λίστα των χρηστών, ώστε να εντοπίσουμε σε ποιον ανήκει
        # ο μοναδικός αριθμός που είναι αποθηκευμένος στο session cookie.
        for user in users:
            if user[0] == session['user_id']:
                # Αποθηκεύουμε τη λίστα που αφορά τα στοιχεία του χρήστη
                # στο g.user, ώστε να είναι προσβάσιμα από όλες τις σελίδες.
                g.user = user
                # Με τον ίδιο τρόπο που γνωστοποιούμε
                # τα στοιχεία του χρήστη σε όλες τις σελίδες,
                # γνωστοποιούμε και το αντικείμενο s ώστε
                # να έχουμε πρόσβαση στα δεδομένα του Sense HAT
                g.s=s

# H @app.route() της βιβλιοθήκης Flask  εκτελεί τη συνάρτηση που ακολουθεί,
# ανάλογα με τη διευθυνση URL που επισκέπτεται ο χρήστης

@app.route('/')
def index():
    if not g.user:
        return redirect(url_for('logme'))
    return render_template('index.html')

#########logme##############

# Χρησιμοποιούμε το όρισμα methods για να δηλώσουμε ότι:
# μπορούμε να δεχθούμε δεδομένα από τη φόρμα μας.

@app.route('/logme', methods=['POST','GET'])
def logme():
    # Μόλις ένας χρήστης επισκέπτεται τη σελίδα login
    # αφαιρούμε το τυχόν session cookie που έχει
    # αποθηκευτεί στον υπολογιστή του χρήστη.
    # Το πετυχαίνουμε αυτό με τη session.pop:
    session.pop('user_id', None)
    # Τα περιεχόμενα της παρακάτω if θα εκτελεστούν όταν ο
    # χρήστης επιλέξει το κουμπί ΕΙΣΟΔΟΣ.
    if request.method=='POST':
        # Αποθηκεύουμε το username και τον κωδικό
        # από το χρήστη που συμπλήρωσε τη φόρμα.
        username = request.form['username']
        password = request.form['password']
        for user in users:
           # Διατρέχουμε τη λίστα των χρηστών για να ελέγξουμε αν υπάρχει
           # χρήστης σύμφωνα με τα στοιχεία που λάβαμε από την φόρμα:
            if user[1]==username and user[2]==password:
                # Αν τα στοιχεία που έχει δώσει ο χρήστης είναι σωστά,
                # τότε δημιουργούμε ένα session cookie με όνομα user_id
                # και αποθηκεύουμε εκεί το μοναδικό return render_template('index.html')ριθμό που αντιστοιχεί
                # στο χρήστη.
                session['user_id'] = user[0]
                # Έπειτα δρομολογούμε το χρήστη στη σελίδα που θα
                # είναι διαθέσιμα τα δεδομένα του sense HAT.
                return redirect(url_for('index'))

    return render_template('login.html')

########sense######
@app.route('/sense')
def sense_data():
    if not g.user:
        return redirect(url_for('logme'))
    return render_template('info.html')

#########context_processor##############

@app.context_processor
# Αρχικά φτιάχνουμε μια βασική συνάρτηση:
def a_processor():
    # Μέσα στη βασική συνάρτηση υλοποιούμε μια συνάρτηση με όνομα
    # roundv()  (ή κάποιο άλλο όνομα της επιλογής σας) που δέχεται
    # δύο ορίσματα: μια τιμή και το πλήθος των δεκαδικών ψηφίων.
    def roundv(value,digits):
        # Τα ορίσματα αυτά τα περνάμε στη συνάρτηση round() της
        #  python, η οποία κάνει τη ζητούμενη εργασία.
        return round(value,digits)
    # Τέλος, η βασική συνάρτηση επιστρέφει υπό μορφή λεξικού το όνομα της
    # συνάρτησης roundv() που υλοποιήσαμε, ώστε να είναι διαθέσιμη στα templates.
    return {'roundv':roundv}

###############ships#######################
@app.route('/ships',methods=['POST','GET'])
def ships():
    if not g.user:
        return redirect(url_for('logme'))
    if request.method=='POST':
        x=int(request.form['x'])
        y=int(request.form['y'])
        print(x,y)
        if x>7:
            RandomShips()
        else:
            turn_on(x,y)
    return render_template('ships.html')

############bonus_ships#########################
@app.route('/bonus_ships',methods=['POST','GET'])
def bonus_ships():

    if not g.user:
        return redirect(url_for('logme'))

    if g.user[0] % 2 ==1:
        g.color="ΜΠΛΕ"
        g.point='(1x0)'
    else:
        g.color="ΚΟΚΚΙΝΟ"
        g.point='(0x1)'

    if request.method=='POST':
        x=int(request.form['x'])
        y=int(request.form['y'])
        print(x,y)
        g.comment="                                          "

        if x>7:
            y=0
            RandomShips()
        #elif x<0 or y>7:
            #g.comment="Λανθασμένη είσοδος. Δοκιμάστε ξανά"
        elif (-1<x and x<8) and (-1<y and y<8):
            turn_bonus_on(x,y)
        else:
            g.comment="Λανθασμένη είσοδος. Δοκιμάστε ξανά"

    g.red=count_colour(red)
    g.blue = count_colour(blue)
    g.bluesuc = count_colour(light_blue)
    g.redsuc=count_colour(yellow)
    g.green = count_colour(green)
    g.active_game=(g.green==0)

    return render_template('bonus_ships.html')

##########turn_on ###############
def turn_on (x,y):
    if s.get_pixel(x,y)==green:
        s.set_pixel(x,y,red)
    else:
        s.set_pixel(x,y,blue)

###########turn_bonus_on############
def turn_bonus_on (x,y):

    if int(g.user[0] % 2==1):
        if s.get_pixel(x,y)==green:
            s.set_pixel(x,y,light_blue)
        else:
            s.set_pixel(x,y,blue)

    if int(g.user[0] % 2==0):
        if s.get_pixel(x,y)==green:
            s.set_pixel(x,y,yellow)
        else:
            s.set_pixel(x,y,red)
#########count_colour###########
def count_colour(colour):
    c = 0
    for i in range(0,8):
        for k in range(0,8):
            #print(i,k, s.get_pixel(i,k),c)
            if s.get_pixel(i,k) == colour:
                c=c+1
    return c

#########RandomShips#########
def RandomShips():
    s.clear()
    shipmap=[green]*10+[black]*54
    random.shuffle(shipmap)
    s.set_pixels(shipmap)

if __name__ == '__main__' :
    app.run(debug=True)
