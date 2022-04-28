import csv
import os, sys
import math 

import matplotlib.pyplot as plt
import numpy as np

import re 

def menu():

    print()
    choice = input("""
    A: Scan
    Q: Fermer

    Please enter your choice: """)

    if choice == "A" or choice =="a":
        main()    
      
    elif choice=="Q" or choice=="q":
        sys.exit
    else:
        menu()


def main():
    with open('db.csv', newline='', encoding="utf8") as csvfile:
        data = csv.DictReader(csvfile, delimiter=';')

        #Mots clés
        accessibilite_pmr_correct = ["Accessibilité inconnue","Non accessible","Accessible mais non réservé PMR", "Réservé PMR"]
        #Pour voir les champs 
        # header = []
        # header = next(data)
        # print(header)


        global errorKey, errorOther, ligne, test, errorOther, ligne_incorrect, ligne_correct, ligne_utilisable, compteur
        errorKey = 0 
        errorOther = 0 
        ligne = 1
        test = 0 
        ligne_incorrect = 0 
        ligne_correct = 0 
        ligne_utilisable = 0 
        compteur = 0 


        for row in data:
            checkKey(row, accessibilite_pmr_correct)
            print(errorKey)
            print(errorOther)
            print(2 * "\n") 
            # print(row['nom_amenageur'])
            compteur +=1

        print(3 * "\n")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Nombre de lignes : "+str(compteur))
        print("Lignes incorrectes : " + str(ligne_incorrect))
        print("Lignes correctes : " + str(ligne_correct))
        print("Lignes utilisables : " + str(ligne_utilisable))
        calculPourcentage()
        graph(ligne_incorrect,ligne_correct,ligne_utilisable)
        menu()

def checkKey(row, accessibilite_pmr_correct):
    #print(row['accessibilite_pmr'])
    #if not accessibilite_pmr or accessibilite_pmr == "Accessibilité inconnue" or accessibilite_pmr == "Non accessible" or accessibilite_pmr == "Accessible mais non réserv PMR": 
    global errorKey, errorOther, ligne, test, errorOther, ligne_incorrect, ligne_correct, ligne_utilisable
    errorKey = 0 
    ligne +=1 
    #print("ligne : "+ str(ligne) +" , "+ str(row['accessibilite_pmr'])+ " , "+ str(row['code_insee_commune'])+ " , " + str(row['horaires]))

    print("Vérification des champs clés de la ligne : " + str(ligne))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    print("Vérification accessibilite_pmr ...")
    #Si le champs est vide
    if row['accessibilite_pmr'] not in accessibilite_pmr_correct:
        #print(row['accessibilite_pmr'])
        errorKey = 1

    print("Vérification code_insee_commune ...")
    #if str(len(row['code_insee_commune'])) != 5 and row['code_insee_commune'] << 0 and row['code_insee_commune'] >> 100000:
    #Si la taille du champs n'est pas égale à 5
    if len(row['code_insee_commune']) != 5 :
        #print(row['code_insee_commune'])
        errorKey = 1

    print("Vérification coordonneesXY ...")
    x = re.search("^\[([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?,.*[0-9]*\.[0-9]+\]$", row['coordonneesXY'])
    if x:
        print("Coordonnées correctes")
    else:
        print("Coordonnées incorrectes")
        errorKey = 1
    
    print("Vérification horaires ...")
    if row['horaires'] != "24-juil":
        errorKey = 1  

    print("Vérification id_station_itinerance ...")
    z = re.search("^[a-zA-Z]+.*$", row['id_station_itinerance'])
    if z:
        print("id_station_itinerance correct")
    else:
        print("id_station_itinerance incorrect")
        errorKey = 1

    print("Vérification prise_type_ef ...")
    if not row['prise_type_ef'] or row['prise_type_ef'] != "true" and row['prise_type_ef'] != "false" :
        errorKey = 1

    print("Vérification prise_type_2 ...")
    if not row['prise_type_2'] or row['prise_type_2'] != "true" and row['prise_type_2'] != "false" :
        errorKey = 1  

    print("Vérification prise_type_combo_ccs ...")
    if not row['prise_type_combo_ccs'] or row['prise_type_combo_ccs'] != "true" and row['prise_type_combo_ccs'] != "false" :
        errorKey = 1     

    print("Vérification prise_type_chademo ...")
    if not row['prise_type_chademo'] or row['prise_type_chademo'] != "true" and row['prise_type_chademo'] != "false" :
        errorKey = 1     

    print("Vérification prise_type_autre ...")
    if not row['prise_type_autre'] or row['prise_type_autre'] != "true" and row['prise_type_autre'] != "false" :
        errorKey = 1     

    print("Vérification restriction_gabarit ...")
    if not row['restriction_gabarit']:
        errorKey = 1   

    print("Vérification station_deux_roues ...")
    if not row['station_deux_roues'] or row['station_deux_roues'] != "true" and row['station_deux_roues'] != "false" :
        errorKey = 1     


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #On vérifie si la variable errorKey est égale à 1, Si oui, la ligne est incorrect
    if errorKey == 1:
        print("Champs incorrect ...")
        ligne_incorrect+=1
    else: 
        checkOther(row)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def checkOther(row):
    global errorKey, errorOther, ligne, test, errorOther, ligne_incorrect, ligne_correct, ligne_utilisable
    liste_implantation_station = ["Voirie", "Parking privé à usage public", "Parking privé réservé à la clientèle", "Parking public", "Station dédiée à la recharge rapide"]
    liste_raccordement = ["Direct", "Indirect"]
    errorOther = 0 

    print("Vérification des champs de la ligne : " + str(ligne))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    print("Vérification nom_amenageur ...")
    if not row['nom_amenageur']:
        errorOther = 1

    print("Vérification gratuit ...")
    if not row['gratuit'] or row['gratuit'] != "true" and row['gratuit'] != "false" :
        errorOther = 1     

    print("Vérification paiement_acte ...")
    if not row['paiement_acte'] or row['paiement_acte'] != "true" and row['paiement_acte'] != "false" :
        errorOther = 1     

    print("Vérification paiement_cb ...")
    if not row['paiement_cb'] or row['paiement_cb'] != "true" and row['paiement_cb'] != "false" :
        errorOther = 1     

    print("Vérification paiement_autre ...")
    if not row['paiement_autre'] or row['paiement_autre'] != "true" and row['paiement_autre'] != "false" :
        errorOther = 1    
     
    print("Vérification siren_amenageur ...")
    if len(row['siren_amenageur']) != 9:
        errorOther = 1    

    print("Vérification contact_amenageur ...")
    x = re.search("^.*@.*\.[a-zA-Z]+$", row['contact_amenageur'])
    if x:
        print("Contact correct")
    else:
        print("Contact incorrect")
        errorOther = 1
        
    print("Vérification nom_operateur ...")
    if not row['nom_operateur'] :
        errorOther = 1    

    print("Vérification contact_operateur ...")
    x = re.search("^.*@.*\.[a-zA-Z]+$", row['contact_operateur'])
    if x:
        print("Contact opérateur correct")
    else:
        print("Contact opérateur incorrect")
        errorOther = 1

    print("Vérification telephone_operateur ...")
    if not row['telephone_operateur'] :
        errorOther = 1  
    
    print("Vérification nom_enseigne ...")
    if not row['nom_enseigne'] :
        errorOther = 1  
    
    print("Vérification id_station_local ...")
    if not row['id_station_local'] :
        errorOther = 1  

    print("Vérification nom_station ...")
    if not row['nom_station'] :
        errorOther = 1 
    
    print("Vérification implantation_station  ...")
    if row['implantation_station'] not in liste_implantation_station:
        errorOther = 1 

    print("Vérification adresse_station ...")
    if not row['adresse_station'] :
        errorOther = 1

    print("Vérification nbre_pdc ...")
    x = re.search("\d", row['nbre_pdc'])
    if x:
        print("nbre_pdc correct")
    else:
        print("nbre_pdc incorrect")
        errorOther = 1

    print("Vérification id_pdc_itinerance ...")
    if not row['id_pdc_itinerance'] :
        errorOther = 1

    print("Vérification id_pdc_local ...")
    if not row['id_pdc_local'] :
        errorOther = 1

    print("Vérification puissance_nominale ...")
    x = re.search("^[0-9]*\.[0-9]+$", row['puissance_nominale'])
    if x:
        print("puissance_nominale correct")
    else:
        print("puissance_nominale incorrect")
        errorOther = 1

    print("Vérification tarification ...")
    if not row['tarification'] :
        errorOther = 1

    print("Vérification condition_acces ...")
    if row['condition_acces'] != "Accès libre" and row['condition_acces'] != "Accès réservé" :
        errorOther = 1

    print("Vérification reservation ...")
    if not row['reservation'] or row['reservation'] != "true" and row['reservation'] != "false" :
        errorOther = 1   

    print("Vérification raccordement  ...")
    if row['raccordement'] not in liste_raccordement:
        errorOther = 1 

    print("Vérification num_pdl ...")
    if not row['num_pdl'] :
        errorOther = 1 

    print("Vérification date_mise_en_service ...")
    x = re.search("^.*/.*/.*$", row['date_mise_en_service'])
    if x:
        print("date_mise_en_service correct")
    else:
        print("date_mise_en_service incorrect")
        errorOther = 1

    print("Vérification date_maj ...")
    x = re.search("^.*/.*/.*$", row['date_maj'])
    if x:
        print("date_maj correct")
    else:
        print("date_maj incorrect")
        errorOther = 1


    print("Vérification last_modified ...")
    x = re.search("^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?([zZ]|([\+-])([01]\d|2[0-3]):?([0-5]\d)?)?$", row['last_modified'])
    if x:
        print("last_modified correct")
    else:
        print("last_modified incorrect")
        errorOther = 1

    if len(row['datagouv_dataset_id']) != 24 :
        errorOther = 1

    if len(row['datagouv_resource_id']) != 36 :
        errorOther = 1

    print("Vérification datagouv_organization_or_owner ...")
    if not row['datagouv_organization_or_owner'] :
        errorOther = 1 

    print("Vérification consolidated_longitude ...")
    x = re.search("^([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?$", row['consolidated_longitude'])
    if x:
        print("consolidated_longitude correct")
    else:
        print("consolidated_longitude incorrect")
        errorOther = 1

    print("Vérification consolidated_latitude ...")
    x = re.search("^([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?$", row['consolidated_latitude'])
    if x:
        print("consolidated_latitude correct")
    else:
        print("consolidated_latitude incorrect")
        errorOther = 1

    if len(row['consolidated_code_postal']) != 5 :
        errorOther = 1

    print("Vérification consolidated_commune ...")
    if not row['consolidated_commune'] :
        errorOther = 1

    print("Vérification consolidated_is_lon_lat_correct ...")
    if row['consolidated_is_lon_lat_correct'] != "True" and row['consolidated_is_lon_lat_correct'] != "False" :
        errorOther = 1   

    print("Vérification consolidated_is_code_insee_verified ...")
    if row['consolidated_is_code_insee_verified'] != "True" and row['consolidated_is_code_insee_verified'] != "False" :
        errorOther = 1   

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #On vérifie si ces champs sont corrects ou non, si non la ligne devient utilisable 
    if errorOther == 1:
        print("Champs utilisable mais pas correct ...")
        ligne_utilisable += 1 
    else: 
        print("Champs correct ...")
        ligne_correct += 1
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def calculPourcentage(): 
    global ligne_incorrect, ligne_correct, ligne_utilisable, compteur

    pourcentage_incorrect = math.floor((ligne_incorrect / compteur) * 10000) / 100
    pourcentage_correct = math.floor((ligne_correct / compteur) * 10000) / 100
    pourcentage_utilisable = math.floor((ligne_utilisable / compteur) * 10000) / 100

    print("Pourcentage incorrect : " + str(pourcentage_incorrect) + " %")
    print("Pourcentage correct : " + str(pourcentage_correct) + " %" )
    print("Pourcentage utilisable : " + str(pourcentage_utilisable) + " %")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
   	

def graph(ligne_incorrect,ligne_correct,ligne_utilisable): 

    choice = input("""
    A: Afficher le graph
    Q: Fermer

    Please enter your choice: """)

    if choice == "A" or choice =="a":
        Product = ['Lignes incorrectes','Lignes correctes','Lignes utilisables']
        #Lignes = ['1000', '2000', '3000', '4000', '5000', '6000', '7000', '8000', '9000', '10000']
        Quantity = [ligne_incorrect,ligne_correct,ligne_utilisable]

        hbars = plt.barh(Product,Quantity,)
        plt.bar_label(hbars, padding=8, color='r', fontsize=8)
        plt.title('')
        plt.ylabel('')
        plt.xlabel('')
        plt.show()    
    else:
        sys.exit()

def findDoublon(): 
    print("")

menu()


