from utils import log
import controller
import login



def add_route(webapp):
    login.add_route(webapp)
    controller.add_route(webapp)
    log.logger.info('contract add route end')
