from cassandra.cluster import Cluster


class Connexion:
    def __init__(self):
        self.cluster = Cluster(['127.0.0.1'], port=9042)
        self.session = self.cluster.connect('gestion_etudiants')

    def recherMatiere(self, LENomMa):
        bd = '''
                 SELECT nom_mat, id_mat FROM  matiere where nom_mat ='{}'  
                 ALLOW FILTERING;
                 '''.format(LENomMa)
        resultat = self.session.execute(bd)
        j = 0
        for i in resultat:
            j = j + 1
            if i[0] != "":
                return i
        return "Nane"

    def insert_etudiant(self, CNE, code_apoge, email, nom, prenom, ville, region):
        try:
            bd = "INSERT INTO etudiant (code_apoge ,CNE ,email ,nom ,prenom, addresses) VALUES ('" + code_apoge  + "','" + CNE + "','" + email + "','" + nom + "','" + prenom + "',{ ville: '" + ville + "', region: '" + region + "'});"
            self.session.execute(bd)
        except Exception as e:
            print(e)

    def select_table_Etudiant(self):
        bd = '''
                 SELECT code_apoge ,CNE ,email ,nom ,prenom, 
                 addresses.ville, addresses.region  FROM etudiant
                 '''
        resultat = self.session.execute(bd)
        return resultat

    def insert_Matiere(self, nom_mat, coeff):
        bd = '''
               INSERT INTO matiere (
                        id_mat  ,
                        nom_mat,
                        coefficient
                        ) VALUES (uuid(),'{}',{});
               '''.format(nom_mat, coeff)
        self.session.execute(bd)

    def insert_Note_By_Etudiant(self, id_mat, code_apoge, note):
        bd = '''
               INSERT INTO note_by_etudiant (
                    code_apoge   ,
                    id_mat  ,
                    note
                    ) VALUES ('{}', {},{});
               '''.format(code_apoge, id_mat, note)
        self.session.execute(bd)

    def insert_Note_By_Matiere(self, id_mat, code_apoge, note):
        bd = '''
               INSERT INTO note_by_matiere (
                    id_mat  ,
                    code_apoge   ,
                    note
                    ) VALUES ({},'{}',{});
               '''.format(id_mat, code_apoge, note)
        self.session.execute(bd)

    def recher_codeapoge(self, code_apoge):
        bd = '''
                 SELECT code_apoge FROM  etudiant where code_apoge ='{}'  
                 ALLOW FILTERING;
                 '''.format(code_apoge)
        resultat = self.session.execute(bd)
        for i in resultat:
            return i[0]
        return "Nane"

    def select_Etudiant(self, code_apoge):

        if code_apoge == "":
            bd = '''
                     SELECT code_apoge ,CNE ,email ,nom ,prenom, addresses.ville, addresses.region  FROM etudiant 
                     '''
            resultat = self.session.execute(bd)
            return resultat
        else:
            bd = '''
                    SELECT code_apoge ,CNE ,email ,nom ,prenom, addresses.ville, addresses.region  FROM etudiant
                     WHERE code_apoge ='{}' ALLOW FILTERING;
                    '''.format(code_apoge)
            resultat = self.session.execute(bd)
            return resultat

    def selectmoyene(self):
        bd = '''
            SELECT average(note) from note_by_matiere;
                         '''
        resultat = self.session.execute(bd)
        return resultat

    def calcule_moyenne(self, code_apoge):
        try:
            liste_id_matire = []
            liste_note = []
            list_coef = []
            bd = '''
                  select id_mat,note from note_by_etudiant where code_apoge='{}' ALLOW FILTERING;
                '''.format(code_apoge)
            resultat = self.session.execute(bd)
            for row in resultat:
                liste_id_matire.append(row[0])
                liste_note.append(row[1])

            for i in liste_id_matire:
                bd = '''
                              select coefficient from matiere where id_mat={} ALLOW FILTERING;
                            '''.format(i)
                rows = self.session.execute(bd)

                for row in rows:
                    list_coef.append(row[0])
            moyenne = 0
            if (len(list_coef) == 0):
                return 'pas de note'
            else:
                for indice in range(len(liste_note)):
                    moyenne = moyenne + (liste_note[indice] * list_coef[indice])
                return round(moyenne / sum(list_coef), 2)


        except Exception as e:
            print(e)
            return "pas de note"