
from core       import Core
from synop      import Synop
from scenario   import Scenario
from conti      import Conti
from ppt        import PPT



class PreprodAI( Core ):
    def __init__( self ):
        self.synop    = ''
        self.scenario = ''
    
    def write_synop( self, *key ):
        Synop().write( key )
        
    def write_scene( self ):
        Scenario().write()

    def draw_conti( self, scenario, scenario_idx ):
        Conti().draw_conti( scenario, scenario_idx )

    def dev_character( self, scenario, scenario_idx ):
        Character().dev_charactire( scenario, scenario_idx )

    def drawing_concept( self, synop ):
        Concept().drawing_concept( synop )

    def set_budget( self, schedule , scenario_idx ):
        Budget().set_budget( schedule , scenario_idx )

    def make_schedule( scenario, scenario_idx ):
        Schedule.make( scenario, scenario_idx )
    
    def write_ppt( self ):
        result = PPT().write()        
        return result








