
from pm4py.algo.filtering.log.start_activities import start_activities_filter
from pm4py.algo.filtering.log.end_activities import end_activities_filter
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.filtering.log.variants import variants_filter
from pm4py.statistics.traces.generic.log import case_statistics
from pm4py.algo.filtering.log.attributes import attributes_filter
 
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer


class Handler():
    
    def fileReader(self, event_log):
        event_log = xes_importer.apply(event_log)
        return event_log
    
    def genaralDataInformation(self, event_log):
        reader = self.fileReader(event_log)
        log_start = start_activities_filter.get_start_activities(reader)
        end_activities = end_activities_filter.get_end_activities(reader)
        
        print(f"Process starts with {len(log_start)} no of activities, and {log_start} activities" )
 
        print(f"Process ends with {len(end_activities)} no of activities, and {end_activities} activities")
        
        variants = variants_filter.get_variants(reader)
        print(f"Process have {len(variants)} of variants with the logs") 
        
        variants_count = case_statistics.get_variant_statistics(reader)
        variants_count = sorted(variants_count, key=lambda x: x['count'], reverse=True)
        # variants_count[:10]
        print(f"Process variants {len(variants) / len(reader) * 100}% with no of logs")
        
        activities = attributes_filter.get_attribute_values(reader, "concept:name")
        print(f"No of activities {len(activities)} of activities {activities}")
        
    def alphaMiner(self, event_log):
        reader = self.fileReader(event_log)
        net, initial_marking, final_marking = alpha_miner.apply(reader)
        parameters = {pn_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "png"}
        gviz = pn_visualizer.apply(net, initial_marking, final_marking, parameters=parameters, variant=pn_visualizer.Variants.FREQUENCY, log=reader)
        pn_visualizer.save(gviz, "alpha_graph.png")
        pn_visualizer.view(gviz)
        
        
c = Handler()
file = '../bpi_challenge_2017.xes'
count = c.genaralDataInformation(file)
count = c.alphaMiner(file)
print(count)


