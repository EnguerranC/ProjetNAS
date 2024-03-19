import json

""" 
                                                ----------------------------------
                                                --- Generateur du fichier json ---
                                                ----------------------------------

L'essentiel des informations doivent être changées ou rajoutées à la main dans le dico config. Se réferer au Readme pour comprendre sa structure.
Pour rajouter un AS, rajouter juste l'AS et ses caractéristiques dans le dico config et modifier les autres AS pour les éventuels liens.

"""

# Generateur d'une matrice d'adressage vide
def Matrice_addressage_vide(M_ad, N) :
   for i in range(N) :
      M_temp = []
      for j in range(N) :
         M_temp.append(["",""])
      M_ad.append(M_temp)
   return M_ad

# Dictionnaire config à la base de la structure du fichier json
config = {
   1 : { # Numero de l'AS
      "Nombre_routeur" : 4, # Nombre de routeur dans l'AS
      "Type_AS" : "AS", # Type de l'AS (AS, Client, Peer ou Provider)
      "Matrice_adjacence" : [[0,1,0,0],
                             [1,0,1,0],
                             [0,1,0,1],
                             [0,0,1,0]],
      "Masque_reseau" : "192.168.0.0/28",
      "Matrice_adressage_interface" : Matrice_addressage_vide([], 4),
      "Donnees_routeurs" : {
      },
      "Routage_intraAS" : { # Infos concernant le routage intraAS
         "Protocol" : "OSPF"
      },
      "Routage_interAS":{ # Infos concernant le routage interAS
         1 : { # Numero du routeur bordeur
            2 : { # Numero de l'AS remote
               "Num_routeur_bordeur_remote" : 1, # Numero du routeur remote
               "Adresse" : "192.168.1.1/30", # Adresse de l'interface liée au routeur remote
               "Interface" : "" # Interface liée au routeur remote
            },
            3 : { # Numero de l'AS remote
               "Num_routeur_bordeur_remote" : 1, # Numero du routeur remote
               "Adresse" : "192.168.2.1/30", # Adresse de l'interface liée au routeur remote
               "Interface" : "" # Interface liée au routeur remote
            }
         },
         4 : {
            4 : {
               "Num_routeur_bordeur_remote" : 1,
               "Adresse" : "192.168.3.1/30",
               "Interface" : ""
            },
            5 : { # Numero de l'AS remote
               "Num_routeur_bordeur_remote" : 1, # Numero du routeur remote
               "Adresse" : "192.168.4.1/30", # Adresse de l'interface liée au routeur remote
               "Interface" : "" # Interface liée au routeur remote
            }
         }
      }
   },
   2 : {
      "Nombre_routeur" : 1,
      "Type_AS" : "ClientA",
      "Matrice_adjacence" : [[0]],
      "Masque_reseau" : "0.0.0.0/28",
      "Matrice_adressage_interface" : Matrice_addressage_vide([], 1),
      "Donnees_routeurs" : {
      },
      "Routage_intraAS" : {
         "Protocol" : "OSPF"
      },
      "Routage_interAS":{
         1 : {
            1 : {
               "Num_routeur_bordeur_remote" : 1,
               "Adresse" : "192.168.1.2/30",
               "Interface" : ""
            }
         }
      }
   },
   3 : {
      "Nombre_routeur" : 1,
      "Type_AS" : "ClientA",
      "Matrice_adjacence" : [[0]],
      "Masque_reseau" : "0.0.0.0/28",
      "Matrice_adressage_interface" : Matrice_addressage_vide([], 1),
      "Donnees_routeurs" : {
      },
      "Routage_intraAS" : {
         "Protocol" : "OSPF"
      },
      "Routage_interAS":{
         1 : {
            1 : {
               "Num_routeur_bordeur_remote" : 4,
               "Adresse" : "192.168.2.2/30",
               "Interface" : ""
            }
         }
      }
   },
   4 : {
      "Nombre_routeur" : 1,
      "Type_AS" : "ClientB",
      "Matrice_adjacence" : [[0]],
      "Masque_reseau" : "0.0.0.0/28",
      "Matrice_adressage_interface" : Matrice_addressage_vide([], 1),
      "Donnees_routeurs" : {
      },
      "Routage_intraAS" : {
         "Protocol" : "OSPF"
      },
      "Routage_interAS":{
         1 : {
            1 : {
               "Num_routeur_bordeur_remote" : 4,
               "Adresse" : "192.168.3.2/30",
               "Interface" : ""
            }
         }
      }
   },
   5 : {
      "Nombre_routeur" : 1,
      "Type_AS" : "ClientB",
      "Matrice_adjacence" : [[0]],
      "Masque_reseau" : "0.0.0.0/28",
      "Matrice_adressage_interface" : Matrice_addressage_vide([], 1),
      "Donnees_routeurs" : {
      },
      "Routage_intraAS" : {
         "Protocol" : "OSPF"
      },
      "Routage_interAS":{
         1 : {
            1 : {
               "Num_routeur_bordeur_remote" : 1,
               "Adresse" : "192.168.4.2/30",
               "Interface" : ""
            }
         }
      }
   }
}
"""
Generateur de la base de donnee des routeurs : Num_routeur, Nom, Dynamips_ID
Num_routeur : unique dans chaque AS (qui va de 1 à Nombre_routeur)
Nom : unique a tous les routeurs du reseau global et a pour forme AS[Num_AS]_R[Num_routeur]
Dynamips_ID : unique a tous les routeurs du reseau global
"""
Dynamips_ID = 1
for i in range(1,len(config)+1) :
   for j in range(1, config[i]["Nombre_routeur"]+1) :
      Num_routeur = j
      config[i]["Donnees_routeurs"][Num_routeur] = {"Nom":"AS"+str(i)+"_R"+str(j) , "Dynamips_ID":Dynamips_ID}
      Dynamips_ID = Dynamips_ID +1

""" 
Fonction Adressage_AS(Nom_As, Matrice_adjacence, Nombre_routeur) --> None
Configure les adresses et les interfaces des liens d'une AS et inter AS dans le fichier json
Pour trouver les interfaces d'un routeur d'une AS il suffit de lire la ligne correspondant à son numero dans la matrice d'adressage de l'AS
"""
def Adressage_AS(Num_AS , Matrice_adjacence, Nombre_routeur) :
   nb_connexions = [0 for i in range(Nombre_routeur)]
   num_res = 0
   for routeur in range(Nombre_routeur) :
      for lien in range(routeur,Nombre_routeur) :
         if Matrice_adjacence[routeur][lien] :
            nb_connexions[routeur]+=1
            nb_connexions[lien]+=1
            interface1 = "GigabitEthernet" + str(nb_connexions[routeur]) + "/0"
            interface2 = "GigabitEthernet" + str(nb_connexions[lien]) + "/0"

            adresse_unique1 = config[Num_AS]["Masque_reseau"][:7]+".0."+str(num_res+1)+"/30"
            adresse_unique2 = config[Num_AS]["Masque_reseau"][:7]+".0."+str(num_res+2)+"/30"
            config[Num_AS]["Matrice_adressage_interface"][routeur][lien] = [adresse_unique1,interface1]
            config[Num_AS]["Matrice_adressage_interface"][lien][routeur] = [adresse_unique2,interface2]
            num_res += 4
      routeur+=1
      if routeur in list(config[Num_AS]["Routage_interAS"].keys()) :
         for remote_AS in list(config[Num_AS]["Routage_interAS"][routeur].keys()) :
            nb_connexions[routeur-1]+=1
            config[Num_AS]["Routage_interAS"][routeur][remote_AS]["Interface"] = "GigabitEthernet" + str(nb_connexions[routeur-1]) + "/0"

"""
Programme principal
"""
for i in range(len(config)-1) :
   Adressage_AS(i+1, config[i+1]["Matrice_adjacence"], config[i+1]["Nombre_routeur"])

fichier = open("config.json","w") # Creation du fichier json
json.dump(config, fichier, indent=4)
