from labels import *

# TODO : 

'''

'''


class Relation:
    '''
    Contains information about the cause and effect relationship between two drugs.
    '''
    def __init__(self, interaction = None):
        if interaction is None:
            self.subject = None
            self.object = None
            self.description = None
            self.relation = None
            self.normalized_relation = None
        else:
            self.get_relation_from_interaction(interaction)
            self.get_normalized_relation(NORMALIZED_KEYWORDS)
    
    def __repr__(self):
        return 'Subject : {}\nObject : {}\nDescription : {}\nRelation : {}\nNormalized relation :{}'\
    .format(self.subject, self.object, self.description, self.relation, self.normalized_relation)
    
    def get_relation_from_interaction(self, interaction):
        druga = interaction.druga
        drugb = interaction.drugb
        self.description = interaction.description.lower()

        index1 = self.description.find(druga)
        index2 = self.description.find(drugb)

        prefix = ''
        if min(index1, index2) != 0:
            prefix = self.description[:min(index1, index2)]

        if index1 < index2:
            self.subject = druga
            self.object = drugb
            self.relation = prefix + ' ' + self.description[index1 + len(druga): index2].strip()
        else:
            self.subject = drugb
            self.object = druga
            self.relation = prefix + ' ' + self.description[index2 + len(drugb): index1].strip()
        
        if prefix != '':
            self.subject, self.object = self.object, self.subject

    def is_in_order(self, keywords):
        if len(keywords) == 0:
            return True

        index = [self.relation.find(k) for k in keywords]
        
        if index[0] == -1:
            return False
        for i in range(1, len(index)):
            if index[i] == -1 or index[i] < index[i-1]:
                return False
        return True

    def get_normalized_relation(self, normalized_keywords):
        for keywords in normalized_keywords:
            if self.is_in_order(keywords.split()):
                self.normalized_relation = keywords
                return
        
        self.normalized_relation = None

    def is_normalized(self):
        if self.normalized_relation is not None:
            return True
        else:
            return False


def generate_relations(interaction_list):
    '''
    
    '''
    relation_list = []
    for interaction in interaction_list:
        relation = Relation(interaction)
        relation_list.append(relation)
    
    return relation_list
    

def remove_duplicates(relation_list):
    '''

    '''


def filter_unknowns(relation_list):
    '''Filter out Relation objects that don't have a normalized relation


    '''

    filter_count = 0
    new_relation_list = []
    for relation in relation_list:
        if relation.normalized_relation is not None:
            new_relation_list.append(relation)
        elif relation.normalized_relation is None:
            filter_count += 1
        else:
            print(relation.normalized_relation)
    return new_relation_list, filter_count
    # TODO : Output interactions (relation.relation) not being picked up


def generate_labels(relation_list):
    '''Generate numerical labels for each interaction


    '''

    label_map = {}
    label_lookup = {}
    counter = 0
    for relation in relation_list:
        if relation.normalized_relation not in label_map:
            label_map[relation.normalized_relation] = counter
            label_lookup[counter] = relation.normalized_relation
            counter += 1
    
    return label_map, label_lookup