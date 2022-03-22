import qrcode

qr = qrcode.QRCode(
    version=4,
    error_correction=qrcode.constants.ERROR_CORRECT_L, 
    box_size=15,
    border=4,
)

locations = ['Alexander Building', 'Amory Building','Building: One','Byrne House','Clayden Building',
'Clydesdale Court' ,
'Cornwall House', 
'Devonshire House',
'Duckes Meadow Sports Field',
'Exeter Northcott Theatre',
'Exeter Science Park',
'Forum',
'Forum Library',
'Geoffrey Pope Building',
'The Great Hall',
'Haighton Library', 
'Harrison Building',
'Hatherly Building',
'The Henry Wellcome Building for Biocatalysis',
'Hope Hall',
'IAIS Building', 
'Innovation Centre', 
'INTO Building',
'Isambard Parade', 
'Kay Building',
'Kay House Duryard', 
'Knightley',
'Lafrowda Cottage', 
'Laver Building',
'Lazenby House',
'Living Systems Institute',
'Mary Harris Memorial Chapel of the Holy Trinity',
'Newman Building', 
'Nicholas Bull Boathouse',
'Northcote House', 
'Old Library',
'Owlets Nursery', 
'Penryn Campus',
'Peter Chalk Centre',
'Physics Building',
'Queen\'s Building', 
'Reed Hall',
'Reed Mews',
'RILD Building',
'Roborough Building', 
'St. Luke\'s Campus',
'Sir Henry Wellcome Building for Mood Disorders Research', 
'Sports Park',
'Streatham Court',
'Streatham Farm',
'Thornlea Complex',
'Truro Campus',
'Topsham Sports Ground',
'University of Exeter Medical School',
'Washington Singer Building',
'XFi Building']



"""
Creates the qr code for each picture
"""
for location in locations:
    qr.add_data(location)
    qr.make(fit=True)
    img = qr.make_image(back_color="white", fill_color="black")
    img.save(f'{location}.png')
    qr.clear()
