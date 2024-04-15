from flask import Flask, render_template, request

def init_app(app : Flask):
    @app.errorhandler(404)
    def page_not_found(error):
        error = {
            'title' : 'Pagina Non Trovata',
            'description' : 'La pagina che stavi cercando non esiste.'
        }
        return render_template('error.html', status_code=404, error=error), 404
    
    @app.errorhandler(403)
    def forbidden(error):
        error = {
            'title' : 'Accesso Negato',
            'description' : 'Non hai i permessi per accedere a questa pagina.'
        }
        return render_template('error.html', status_code=403, error=error), 403
    
    @app.errorhandler(400)
    def bad_request(error):
        error = {
            'title' : 'Richiesta Non Valida',
            'description' : 'La richiesta che hai inviato non è valida.'
        }
        return render_template('error.html', status_code=400, error=error), 400
    
    @app.errorhandler(500)
    def internal_server_error(error):
        error = {
            'title' : 'Errore del Server',
            'description' : 'Si è verificato un errore interno al server.'
        }
        return render_template('error.html', status_code=500, error=error), 500