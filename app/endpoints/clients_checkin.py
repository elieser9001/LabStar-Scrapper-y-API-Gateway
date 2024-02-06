from flask import Blueprint, jsonify
from app.lib import Auth, Scraper

bp = Blueprint('clients_checkin', __name__)

@bp.route('/checkin_records', methods=['GET'])
def checkin():
    session_manager = Auth.SessionManager()
    scraper = Scraper.LabStar(session_manager=session_manager)
    
    checkin_records = scraper.get_checkin_clients()
    
    return jsonify(checkin_records)

@bp.route('/checkin_details/<int:id>/')
def checkin_details(id):
    session_manager = Auth.SessionManager()
    scraper = Scraper.LabStar(session_manager=session_manager)
    attachments = scraper.get_attachment_by_case(case_id=id)
    case_items = scraper.get_case_items(case_id=id)
    case_instructions = scraper.get_case_instructions(case_id=id)
    case_notes = scraper.get_case_notes(case_id=id)
    case_dr_preferences = scraper.get_case_dr_preferences(case_id=id)
    
    json_case = {
        "case_attachments": attachments,
        "case_items": case_items,
        "case_instructions": case_instructions,
        "case_notes": case_notes,
        "dr_preferences": case_dr_preferences,
    }
    
    return jsonify(json_case)
