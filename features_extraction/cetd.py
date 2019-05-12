import sys
import os
import pandas as pd
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 100)

sys.path.append(os.path.realpath(os.path.abspath('../utilities')))


from dom_mapper import DOM_Mapper




class CETD(DOM_Mapper):
    
    FEATURES_LABELS = ['TEXT_DENSITY', 'DENSITY_SUM', 'VISUAL_IMPORTANCE', 'COMPOSITE_TEXT_DENSITY', 'HYBRID_TEXT_DENSITY']
    
    max_density_sum = 0    
    
    def __init__(self):
        super().__init__()
        pass
    
    
    def apply(self, node):
        
        self.count_tags(node)
        self.text_density(node)
        self.density_sum(node)
        self.max_density_sum(node)
        
        self.thresholding(node)
        self.mark_content(node, node, self.threshold)
        
        pass
    
    
    def count_tags(self, node):
        
        self.map(node, fun1 = self.__init_count_tags, fun3 = self.__count_tags)
        
        pass
    
    
    def __init_count_tags(self, node):
        
        node['tagsCount'] = len(node['children'])
        
        return node
        
        pass
    
    def __count_tags(self, node, child):
        
        node['tagsCount'] += child['tagsCount']
        
        return node,child
        pass
    
    
    def text_density(self, node):
        
        self.map(node, fun1 = self.__text_density)
        
        pass
    
    def __text_density(self, node):
        
        tagsCount = (node['tagsCount'] if node['tagsCount'] > 0 else 1)
        charsCount = 0
        try:
            charsCount = len(node['text'])
        except:
            pass
        
        node['textDensity'] = charsCount/tagsCount
        
        return node
        
        pass
    
    
    def density_sum(self, node):
          
        self.map(node, fun1 = self.__init_density_sum, fun3 = self.__density_sum)
        
        pass
    
    
    def __init_density_sum(self, node):
        
        node['densitySum'] = 0
        
        return node
        
        pass
    
    def __density_sum(self, node, child):
        
        node['densitySum'] += child['textDensity']
        
        return node,child
        pass
    
    
    def max_density_sum(self, node):
        
        self.max_density_sum = self.reduce(node, fun1 = lambda x : x['densitySum'], fun2 = lambda x,y : x if x > y else y)
        
        pass
    
    
    
    def mark_DOM_node(self, node, mark):
        
        node['CETD_mark'] = mark        
        
        for child in node['children']:
            self.mark_DOM_node(child, mark)
        
        pass
     
    
    
    def thresholding(self, root):
        
        threshold = -1.0
        node = self.search_DOM_node(root, att = 'densitySum', value = self.max_density_sum)
        threshold = node['textDensity']
        self.mark_DOM_node(node, 1)
        
        parent = self.xpath_based_node_search(root, node['parent_xpath'])
        
        while parent != None:        
            if (threshold - parent['textDensity']) > -1:
                threshold = parent['textDensity']
                
            self.mark_DOM_node(parent, 2)
            
            parent = self.xpath_based_node_search(root, parent['parent_xpath'])
            pass
        
        self.threshold = threshold
        
        return self.threshold
        
        pass
    
   
    
    def find_max_density_sum_tag(self, root, node):
        
        target = self.search_DOM_node(node, 'densitySum', self.max_density_sum)   
        try:
            if target['CETD_mark'] == 1:
                return None
        except:
            return None
        
        self.mark_DOM_node(target, 1)
        
        parent = self.xpath_based_node_search(root, target['parent_xpath'])
        
        while parent != None:        
                
            parent['CETD_mark'] = 2            
            parent = self.xpath_based_node_search(root, parent['parent_xpath'])
            
            pass
        
        pass
    
    
    def mark_content(self, root, node, threshold):
        
        if node['CETD_mark'] != 1 and (node['textDensity'] - threshold) > -1:
            self.find_max_density_sum_tag(root, node)
                
            for child in node['children']:
                self.mark_content(root, child, threshold)
        
        pass
    
    
    def toning_marks(self, node):
        
        
        pass
    
    
    def __toning_marks(self, node):
        
        pass
    
    
    def visual_importance(self, node):
        #...
        pass
    
    
    def hybrid_text_density(self, node):
        #...
        pass
    
    
    pass




if __name__ == '__main__':
    
# =============================================================================
#    cetd = CETD()
     
#    cetd.retrieve_DOM_tree(os.path.realpath('../datasets/extracted_data/0008.json'))
     
#    cetd.count_tags(cetd.DOM)
#    cetd.text_density(cetd.DOM)
#    cetd.density_sum(cetd.DOM)
#    cetd.max_density_sum(cetd.DOM)
#    
#    cetd.thresholding()
#    cetd.mark_content(cetd.DOM, cetd.threshold)
#    cetd.update_DOM_tree()
#    cetd.apply(cetd.DOM) 
    cetd.update_DOM_tree()
#    arr = cetd.flatten(cetd.DOM, ['tagName','xpath','CETD_mark'])
#    df = pd.DataFrame(arr, columns = ['tagName','xpath','CETD_mark'])
#    print(df[df['CETD_mark'] == "1"])
# =============================================================================
    
    
    pass



