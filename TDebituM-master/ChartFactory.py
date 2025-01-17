from py2neo import Graph
from configuration import *
from dash import html

import sys

try:
    graph = Graph(scheme=NEO4J_SCHEME, host=NEO4J_HOST, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
    print(f"\n-> Connection to the backend {DATABASE}")

except Exception:
    print(sys.exc_info()[1])
    print("No neo4j database connection could be established!" + 
            "Check py2neo parameters in configuration.py\n" +
            "Aborting!")
    sys.exit(1)


class Sunburst:
    '''
    Visualize hierarchical data spanning outward radially from root to leaves. 
    The sunburst sectors are determined by the entries in "labels" or "ids" and in "parents".
    The values associated with each of the sectors is set in the entry "values"
    '''
    def __init__(self, parent="TDType", child="TDSubtype", filter_state="All", filter_party=None, info="TDIncident"):
        '''
        Visualize hierarchical data spanning outward radially from root to leaves. 
        The sunburst sectors are determined by the entries in "labels" or "ids" and in "parents".
        The values associated with each of the sectors is set in the entry "values"

        Args:
            parent (str, optional): [description]. Defaults to "TDType".
            child (str, optional): [description]. Defaults to "TDSubtype".
            filter_state (str, optional): [description]. Defaults to "All".
            filter_party ([type], optional): [description]. Defaults to None.
            info (str, optional): [description]. Defaults to "TDIncident".
        '''

        # Inputs
        self.parent = parent
        self.child = child
        self.info = info  
        self.filter_state = filter_state
        self.filter_party = filter_party

        # Methods
        self.data = self.extract_data_from_query()
        self.parents_keys = list(self.data.keys()) #review: or use parameter
        self.parents_keys.sort() 

        # Outputs (go.Sunburst parameters)
        self.ids = self.get_ids()
        self.parents = self.get_parents()
        self.labels = self.get_labels()
        self.values = self.get_values()


    def extract_data_from_query(self):

        #TODO: create 2 input levels to choose from: parent, child
        if self.filter_state == "All":
            query_filter = ""

        else:
            query_filter = f""" 
                            AND EXISTS {"{"}
                                MATCH (tdi:TDItem)-->(cs:CurrentState)
                                WHERE cs.name = "{self.filter_state}"
                            {"}"}
                            """
        if self.filter_party:
            query_filter += f"""
                            AND EXISTS {"{"}
                                MATCH (p1:Party)-[:INITIATES]->(tdi:TDItem)-[:AFFECTS]->(p:Party)
                                WHERE p1.name = "{self.filter_party}"
                            {"}"}
                            """
        # https://neo4j.com/docs/cypher-manual/current/introduction/uniqueness/ 


        if self.parent == "TDType": #self.child='TDSubtype'
            query = f"""
                    MATCH(tdt: TDType)--(tds: TDSubtype)--(tdi: TDItem)
                        WHERE EXISTS {"{"}
                            MATCH (tdi: TDItem)--(p:Party)
                        {"}"}
                    {query_filter}
                    RETURN tdt.name AS {self.parent}, tds.name AS {self.child}
                    """
            
        elif self.parent == "Party": #self.child='Party'
            query = f"""
                    MATCH(tdt: TDType)--(tds: TDSubtype)--(tdi: TDItem)--(p:Party)
                        WHERE EXISTS {"{"}
                            MATCH (tdi: TDItem)--(p:Party)
                        {"}"}
                    {query_filter}
                    RETURN p.name AS {self.parent}, tdt.name AS {self.child}
                    """
        
        data_query = graph.run(query).data()
    
        data = {}
        for pair in data_query:
            parent = pair[self.parent]
            child = pair[self.child]

            if type(child)==list: #review: this fenomen, is it happening in the new database?
                child = child[0]
            if type(parent)==list:
                parent = parent[0]

            if parent not in data.keys():
                data[parent] = {child: 1}

            else:
                if child not in data[parent]:
                    data[parent][child] = 1
                else:
                    data[parent][child] += 1 #debug: it doesn't count this well

        return data
    
    def get_parents(self):
        output_parents = []
        
        for parent in self.parents_keys:
            output_parents.append("")
            for i in range(len(self.data[parent])):
                output_parents.append(parent)

        return output_parents

    def get_labels(self,max_string=20):
        labels = []

        for parent in self.parents_keys: 
            children = []
            for label in self.data[parent]:
                output_label = Sunburst.split_string_lines(label, max_string)
                children.append(output_label)
            labels += [parent] + children

        return labels

    def get_values(self):
        values = []

        for parent in self.parents_keys:
            values.append(0)  # value of the parent goes before their children
            values_children = []
            for value in self.data[parent].values():
                values_children.append(value)
            values += values_children

        return values
    
    def get_ids(self):
        ids = []

        for parent in self.parents_keys: 
            children = []
            for label in self.data[parent]:
                if label not in ids:
                    children.append(label)
                else:
                    children.append(f"{parent} - {label}")
            ids += [parent] + children

        return ids
    
    def get_info(self, parent_name, child_name):

        info_dict = {}
        list_items = []

        if self.filter_state == "All":
            query_filter = ""

        else:
            query_filter = f""" 
                            AND EXISTS {"{"}
                                MATCH (tdi:TDItem)-->(cs:CurrentState)
                                WHERE cs.name = "{self.filter_state}"
                            {"}"}
                            """
        
        if self.parent == "TDType":
            query = f"""
                    MATCH(tdt: TDType)--(tds: TDSubtype)--(tdi: TDItem)--(c: {self.info})
                    WHERE tdt.name = "{parent_name}" AND tds.name = "{child_name}"
                    {query_filter}
                    RETURN c.name AS Cause
                    """

        else:        
            query = f"""
                    MATCH(tdt: TDType)--(tds: TDSubtype)--(tdi: TDItem)--(c: {self.info})
                    WHERE tdt.name = "{child_name}" AND
                    EXISTS {"{"}
                        MATCH (tdi: TDItem)--(p:Party)
                        WHERE p.name = "{parent_name}"
                    {"}"}
                    {query_filter}
                    RETURN c.name AS Cause
                    """

        data_query = graph.run(query).data()

        for info_pair in data_query:
            item = info_pair["Cause"]
            if item not in info_dict.keys():
                info_dict[item] = 1
            else:
                info_dict[item] += 1

        info = dict(sorted(info_dict.items(), key=lambda x: x[1], reverse=True))

        for item in info.keys():
            if info[item] == 1:
                list_items.append(html.Li(f"{item}"))
            else:
                list_items.append(html.Li(f"{item} ({info[item]})"))
        
        info_content = [html.Ul(id='my-list', children=list_items)]

        return info_content
    
    @staticmethod
    def split_string_lines(string, max_characters_line):
        index = max_characters_line
        split_string = string.split()

        length = 0
        new_line = 0
        position_previous = 0
        lines = [list() for e in range(15)] # num_lines = len(my_string)//index

        for word in split_string:
            length += len(word) + 1 # whitespace
            new_line = length // index
            if new_line > 0:
                length = length - len(' '.join(lines[position_previous])) # reset length
                lines[position_previous + 1].append(word)
            else:
                lines[position_previous].append(word)
            position_previous += new_line

        output_label = ""
        for line in lines:
            if line != []:
                output_label += ' '.join(line) + '<br>'

        return output_label



class BubbleChart:
    def __init__(self,relationship='INITIATES', state='All'):
        self.relationship = relationship
        self.filter = state

        # Methods
        self.data = self.extract_data_from_query()
        if self.filter != 'All':
            self.data_with_filter = self.extract_data_from_query(subquery=True)

        # Outputs
        self.x = self.extract_x_values()
        self.y = self.extract_y_values()
        self.amount = self.extract_amount()
        self.colors = self.define_colors()


    def extract_data_from_query(self, subquery=False):
        if subquery:
            if self.filter != 'All':
                query_filter = f""" 
                                    AND EXISTS {"{"}
                                        MATCH (tdi:TDItem)-->(cs:CurrentState)
                                        WHERE cs.name = "{self.filter}"
                                    {"}"}
                                    """
            else:
                query_filter = ""
        else:
            query_filter = ""

        query = f"""
                MATCH(tdt: TDType)--(tds: TDSubtype)--(tdi: TDItem)-[rel]-(p:Party)
                WHERE type(rel)="{self.relationship}"
                {query_filter}
                RETURN p.name AS Party, tdt.name AS TDType, tds.name AS TDSubtype
                """
        result = graph.run(query)
        data_query = result.data()

        data = {}
        for pair in data_query:
            x = pair['Party']
            y = pair['TDType']
            info = pair['TDSubtype']
            #info = pair['TDMeasures']

            # if type(child)==list: #review: this fenomen, is it happening in the new database?
            #     child = child[0]
            # if type(parent)==list:
            #     parent = parent[0]

            if x not in data.keys():
                data[x] = {y: [info]}

            else:
                if y not in data[x]:
                    data[x][y] = [info]
                else:
                    data[x][y].append(info) #debug: it doesn't count this well

        return data

    def extract_x_values(self):
        x_values = []
        for party in PARTIES:
            for td_type in TD_TYPES:
                x_values.append(td_type)
        if self.filter != 'All':
            for party in PARTIES:
                for td_type in TD_TYPES:
                    x_values.append(td_type)

        return x_values
    
    def extract_y_values(self):
        y_values = []
        for party in PARTIES:
            for td_type in TD_TYPES:
                y_values.append(party)
        if self.filter != 'All':
            for party in PARTIES:
                for td_type in TD_TYPES:
                    y_values.append(party)

        return y_values
    
    def extract_amount(self):
        amounts = []
        for party in PARTIES:
            for td_type in TD_TYPES: #todo: change tdsubtype, causes, measurements
                if party in self.data.keys():
                    if td_type in self.data[party].keys():
                        amount = len(self.data[party][td_type])
                        amounts.append(amount)
                    else:
                        amounts.append(0)
                else:
                    amounts.append(0)
        if self.filter != 'All':
            for party in PARTIES:
                for td_type in TD_TYPES: #todo: change tdsubtype, causes, measurements
                    if party in self.data_with_filter.keys():
                        if td_type in self.data_with_filter[party].keys():
                            amount = len(self.data_with_filter[party][td_type])
                            amounts.append(amount)
                        else:
                            amounts.append(0)
                    else:
                        amounts.append(0)

        return amounts
    
    def extract_info(self, party, td_type):

        info_dict = {}
        list_items = []
        
        if self.filter != 'All':
            query_filter = f""" 
                                AND EXISTS {"{"}
                                    MATCH (tdi:TDItem)-->(cs:CurrentState)
                                    WHERE cs.name = "{self.filter}"
                                {"}"}
                                """
        else:
            query_filter = ""

        query = f"""
                MATCH(tdt: TDType)--(tds: TDSubtype)--(tdi: TDItem)-[rel]-(p:Party)
                WHERE tdt.name = "{td_type}" AND p.name = "{party}" AND type(rel)="{self.relationship}"
                {query_filter}
                RETURN p.name AS Party, tdt.name AS TDType, tds.name AS TDSubtype
                """
        data_query = graph.run(query).data()

        for info_pair in data_query:
            item = info_pair["TDSubtype"]
            if item not in info_dict.keys():
                info_dict[item] = 1
            else:
                info_dict[item] += 1

        info = dict(sorted(info_dict.items(), key=lambda x: x[1], reverse=True))

        for item in info.keys():
            if info[item] == 1:
                list_items.append(html.Li(f"{item}"))
            else:
                list_items.append(html.Li(f"{item} ({info[item]})"))
        
        info_content = [html.Ul(id='my-list', children=list_items)]

        return info_content

    def define_colors(self):
        colors = []
        for party in PARTIES:
            for td_type in TD_TYPES:
                colors.append('rgb(93, 164, 214)')

        if self.filter != 'All':   
            for party in PARTIES:
                for td_type in TD_TYPES:
                    colors.append('rgb(255, 144, 14)')
        
        return colors


class Sankey:
    '''[summary]
    '''
    def __init__(self, party="All"):
        '''[summary]

        Args:
            party (str, optional): [description]. Defaults to "All".
        '''
        self.parent = party
        self.data = self.extract_data_from_query()

        #outputs
        self.labels = self.get_labels()
        self.source = self.get_source()
        self.target = self.get_target()
        #self.customdata = self.get_info()
        self.value = self.get_values() 
        #self.value = [len(e) for e in self.customdata]
        self.color_link = self.get_color_links()
        self.color_node = self.get_colors_node()
    

    def extract_data_from_query(self):
        if self.parent == 'All':
            additional_filter = ""
        else:
            additional_filter = "WHERE p1.name=$party"

        query = f"""
                MATCH (p1:Party)-[:INITIATES]->(tdi:TDItem)-[:AFFECTS]->(p2:Party)
                {additional_filter}
                RETURN p1.name AS Party, p2.name AS PartyAffected, count(*) AS TDAmount
                """
        data_query = graph.run(query, party=self.parent).data()

        # current_time = datetime.now().strftime("%H:%M:%S")
        # print(current_time + "- sankey main data fetched")

        return data_query
    

    def get_labels(self):
        inputs = []
        outputs = []

        for data_pair in self.data:
            input = data_pair['Party'] + '_I'
            output = data_pair['PartyAffected'] + '_A'

            if input not in inputs:
                inputs.append(input)

            if output not in outputs:
                outputs.append(output)
 
        return inputs + outputs


    def get_source(self):
        source_indexes = []

        for data_pair in self.data:
            input = data_pair['Party'] + '_I'
            source_indexes.append(self.labels.index(input))

        return source_indexes

    def get_target(self):
        target_indexes = []

        for data_pair in self.data:
            output = data_pair['PartyAffected'] + '_A'
            target_indexes.append(self.labels.index(output))

        return target_indexes

    def get_values(self):
        values = []

        for data_pair in self.data:
            output = data_pair['TDAmount']
            values.append(output)

        return values

    
    def get_info(self):

        info = []

        for data_pair in self.data: #debug: this takes too long (2492 entries in self.data)
            input = data_pair['Party']
            output = data_pair['PartyAffected']

            query = """
                MATCH (p1:Party)-[:INITIATES]->(tdi:TDItem)-->(td:TDSubtype)
                WHERE EXISTS {
                    MATCH (p1:Party)-[:INITIATES]->(tdi:TDItem)-[:AFFECTS]->(p2:Party)
                    WHERE p1.name=$party AND p2.name=$cause
                    }
                RETURN td.name AS TD
            """
            info_pair_raw = graph.run(query, party=input, cause=output).data()
            info_pair = list()

            for td in info_pair_raw:
                info_pair.append(td['TD'])
            info.append(info_pair)      

        return info

    def get_color_links(self):
        colors = []
        for e in self.source:
            label = self.labels[e][0:-2]
            colors.append(SANKEY_COLORS[label]) #TODO: define opacity of links
        return colors

    def get_colors_node(self):
        colors = []
        for label in self.labels:
            label = label[0:-2] #change from "ME_I" to "ME"
            if label in SANKEY_COLORS.keys():
                color = SANKEY_COLORS[label]
                colors.append(color[0:-6]+", 1)") #TODO: def change_opacity(color, 1)
            else:
                colors.append("rgba(169,169,169, 1)")

        return colors

class NetworkGraph:
    def __init__(self, incident, display):
        '''[summary]

        Args:
            party (str, optional): [description]. Defaults to "All".
        '''
        self.incident = incident
        self.display = display
        self.nodes = self.extract_nodes()
        self.edges = self.extract_edges()
        self.stylesheet = NetworkGraph.get_stylesheet()
    
    def extract_nodes(self):
        if self.display == 'Cause':
            query = f"""
                    MATCH (tdin:TDIncident)-[r1]-(tdi:TDItem)--(c:Cause)
                    WHERE tdin.name="{self.incident}"
                    RETURN tdin.name AS TDIncident, tdi.ID AS TDItem, c.name AS Cause
                    """
        else:
            query = f"""
                    MATCH (tdin:TDIncident)-[r1]-(tdi:TDItem)--(tds:TDSubtype)--(tdt:TDType)
                    WHERE tdin.name="{self.incident}"
                    RETURN tdin.name AS TDIncident, tdi.ID AS TDItem, tds.name AS TDSubtype, tdt.name AS TDType
                    """

        
        data_query = graph.run(query)

        nodes = []

        for e in data_query:
            
            incident_node = e['TDIncident']
            tdi_node = e['TDItem']
            cause_node = e[self.display]
            
            if incident_node not in nodes:
                nodes.append((incident_node, 'TDIncident'))

            if tdi_node not in nodes:
                nodes.append((tdi_node, 'TDItem'))
            
            if cause_node not in nodes:
                nodes.append((cause_node, 'Cause'))

        return nodes

      
    def extract_edges(self):
        edges = []
        label = "is_part_of"        
        query = f"""
                    MATCH (tdin:TDIncident)-[r1]-(tdi:TDItem)
                    WHERE tdin.name="{self.incident}"
                    RETURN r1 AS Relation1
                    """
        
        data_query = graph.run(query)

        for e in data_query:
            # print(e)
            start_node = e[0].start_node['ID']
            end_node = e[0].end_node["name"]
            # print(start_node)
            # print(end_node)
            edges.append((start_node, end_node, label))

        label = "lead_to"        
        query = f"""
                    MATCH (tdi)-[lt:LEAD_TO]->(tdi2)
                    WHERE EXISTS {"{"}
                        MATCH (tdin:TDIncident)--(tdi:TDItem)
                        WHERE tdin.name="{self.incident}"
                    {"}"}
                    RETURN lt AS LeadTo
                    """
        
        data_query = graph.run(query)

        for e in data_query:
            start_node = e[0].start_node['ID']
            end_node = e[0].end_node["ID"]
            edges.append((start_node, end_node, label))
        
        if self.display == 'Cause':

            label = "has_caused"        
            query = f"""
                        MATCH (tdin:TDIncident)--(tdi:TDItem)-[hc]-(c:Cause)
                        WHERE tdin.name = "{self.incident}"
                        RETURN hc
                        """
        
            data_query = graph.run(query)

            for e in data_query:
                start_node = e[0].start_node['ID']
                end_node = e[0].end_node["name"]
                edges.append((start_node, end_node, label))

        elif self.display == 'TDSubtype':
            label = "belongs_to"        
            query = f"""
                        MATCH (tdin:TDIncident)--(tdi:TDItem)-[r1]-(tds:TDSubtype)
                        WHERE tdin.name = "{self.incident}"
                        RETURN r1
                        """
            data_query = graph.run(query)

            for e in data_query:
                start_node = e[0].start_node['ID']
                end_node = e[0].end_node["name"]
                edges.append((start_node, end_node, label))

        
        elif self.display == 'TDType':
            label = "belongs_to"        
            query = f"""
                        MATCH (tdin:TDIncident)--(tdi:TDItem)-[r1]-(tds:TDSubtype)-[r2]-(tdt:TDType)
                        WHERE tdin.name = "{self.incident}"
                        RETURN r1, r2
                        """
            data_query = graph.run(query)

            for e in data_query:
                start_node = e[0].start_node['ID']
                end_node = e[1].end_node["name"]
                edges.append((start_node, end_node, label))

        return edges
    
    @staticmethod
    def get_stylesheet():
        stylesheet = [
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)'
                }
            },
            {
                'selector': 'edge',
                'style': {
                    'label': 'data(label)',
                    'curve-style': 'bezier',
                }
            },
            {
                'selector': '.TDItem',
                'style': {
                    'background-color': '#79c2d0',
                    
                }
            },
            {
                'selector': '.TDIncident',
                'style': {
                    'shape': 'square',
                    'background-color': '#155263',
                }
            },
            {
                'selector': '.Cause',
                'style': {
                    'background-color': '#ff6f3c',
                }
            },
            {
                'selector': '.lead_to',
                'style': {
                    'target-arrow-color': '#79c2d0',
                    'target-arrow-shape': 'triangle',
                    'line-color': '#79c2d0'
                }
            },
            {
                'selector': '.is_part_of',
                'style': {
                    'target-arrow-color': '#155263',
                    'target-arrow-shape': 'triangle',
                    'line-color': '#155263'
                }
            },
            {
                'selector': '.has_caused',
                'style': {
                    'source-arrow-color': '#ff6f3c',
                    'source-arrow-shape': 'triangle',
                    'line-color': '#ff6f3c'
                }
            },
            {
                'selector': '.belongs_to',
                'style': {
                    'source-arrow-color': '#ff6f3c',
                    'source-arrow-shape': 'triangle',
                    'line-color': '#ff6f3c'
                }
            }
        ]
    
        return stylesheet

class Table:
    '''[summary]
    '''

    def __init__(self, relationship="All", discipline="All", measure="MeasureTaken"):#, id, query=""):
        '''
        The constructor for Table class.

        Args:
            id(str): dash generic id
            query (str, optional): [description]. Defaults to "".
        '''
        # self.id = id
        self.relationship = relationship
        self.discipline = discipline
        self.measure = measure
        self.dataframe = self.extract_data_from_query()
        self.data = self.dataframe.to_dict('records')
        
        #outputs
        # self.table = self.get_dash_data_table()
        self.style_cell = self.get_style_cell()
        self.style_data_conditional = self.get_style_data_conditional()
        self.columns = [{"name": i, "id": i} for i in self.dataframe.columns]
        

    def extract_data_from_query(self):
        if self.relationship == "All":
            query_relationship = f"""
                                (tdi:TDItem)--(p:Party)
                                """ 
            self.name_relationship = "PartiesInvolved"
        else:     
            query_relationship = f"""
                                (tdi:TDItem)-[:{self.relationship}]-(p:Party)
                                """ 
            if self.relationship == "AFFECTS":
                self.name_relationship = "PartiesAffected"
            elif self.relationship == "INITIATES":
                self.name_relationship = "InitiatingParties"

        if self.discipline == "All":
            query_discipline = f"""
                                """ 
        else:     
            query_discipline = f"""
                                AND EXISTS {"{"}
                                    MATCH (tdi:TDItem)-[:AFFECTS]->(p:Party)
                                    WHERE p.name = "{self.discipline}"
                                    {"}"}
                                """


        negation = str("NOT" if self.measure == "MeasureIdeal" else "")
            
        query = f"""
                MATCH (mS:{self.measure})--(tdi:TDItem)--(tds:TDSubtype)--(tdt:TDType),
                (tdi:TDItem)--(tdin:TDIncident),
                {query_relationship}
                WHERE EXISTS {"{"}
                    MATCH (tdi:TDItem)-->(cs:CurrentState)
                    WHERE {negation} cs.name = "Solved"
                    {"}"}
                {query_discipline}
                RETURN  tdi.ID AS ID, tdin.name AS Incident, tdt.name AS TDType, tds.name as TDSubtype, mS.name as {self.measure}, p.name AS {self.name_relationship}
                """

        result = graph.run(query)
        df_data_query = result.to_data_frame()

        if self.discipline == 'All':
            df_data_query = df_data_query.groupby(['ID','Incident','TDType','TDSubtype',self.measure])[self.name_relationship].apply(', '.join).reset_index() # Combine all parties involved


        return df_data_query

    
    def get_style_cell(self):
        style = {
            'whiteSpace': 'normal',
            'height': 'auto',
            'textAlign': 'left',
            # 'backgroundColor': 'rgb(50, 50, 50)',
            # 'color': 'white'
        }
        return style 

    def get_style_data_conditional(self):
        style = [
            {
                'if': {
                    'filter_query': '{TDType} =' + f'"{td}"',
                    'column_id': 'TDType'
                },
                'backgroundColor': TD_TYPES_COLORS[td],
                'color': 'black'
            }
            for td in TD_TYPES]

        return style
