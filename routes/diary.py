import logging
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from models import DiaryEntry
from forms import DiaryEntryForm

# Create blueprint
diary = Blueprint('diary', __name__)
logger = logging.getLogger(__name__)

@diary.route('/')
def index():
    """Render the home page"""
    return render_template('index.html', title='Welcome to Secure Diary')

@diary.route('/dashboard')
@login_required
def dashboard():
    """Render the user dashboard with diary entries"""
    try:
        entries = DiaryEntry.query.filter_by(user_id=current_user.id).order_by(DiaryEntry.created_at.desc()).all()
        return render_template('dashboard.html', title='Your Dashboard', entries=entries)
    except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        flash('An error occurred while loading your dashboard. Please try again.', 'danger')
        return render_template('dashboard.html', title='Your Dashboard', entries=[])

@diary.route('/entry/new', methods=['GET', 'POST'])
@login_required
def create_entry():
    """Create a new diary entry"""
    form = DiaryEntryForm()
    
    if form.validate_on_submit():
        try:
            # Create new entry
            entry = DiaryEntry(user_id=current_user.id)
            entry.title = form.title.data
            entry.content = form.content.data
            
            # Save to database
            db.session.add(entry)
            db.session.commit()
            logger.info(f"New diary entry created: {entry.id} by user {current_user.id}")
            
            flash('Your diary entry has been created!', 'success')
            return redirect(url_for('diary.dashboard'))
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Entry creation error: {str(e)}")
            flash('An error occurred while creating your diary entry. Please try again.', 'danger')
    
    return render_template('create_entry.html', title='New Diary Entry', form=form)

@diary.route('/entry/<int:entry_id>')
@login_required
def view_entry(entry_id):
    """View a specific diary entry"""
    try:
        entry = DiaryEntry.query.get_or_404(entry_id)
        
        # Check if the entry belongs to the current user
        if entry.user_id != current_user.id:
            logger.warning(f"Unauthorized access attempt to entry {entry_id} by user {current_user.id}")
            abort(403)
        
        return render_template('view_entry.html', title=entry.title, entry=entry)
    
    except Exception as e:
        logger.error(f"Entry view error: {str(e)}")
        flash('An error occurred while loading the diary entry. Please try again.', 'danger')
        return redirect(url_for('diary.dashboard'))

@diary.route('/entry/<int:entry_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    """Edit a specific diary entry"""
    try:
        entry = DiaryEntry.query.get_or_404(entry_id)
        
        # Check if the entry belongs to the current user
        if entry.user_id != current_user.id:
            logger.warning(f"Unauthorized edit attempt to entry {entry_id} by user {current_user.id}")
            abort(403)
        
        form = DiaryEntryForm()
        
        if form.validate_on_submit():
            try:
                # Update entry
                entry.title = form.title.data
                entry.content = form.content.data
                entry.updated_at = datetime.utcnow()
                
                # Save to database
                db.session.commit()
                logger.info(f"Diary entry updated: {entry.id} by user {current_user.id}")
                
                flash('Your diary entry has been updated!', 'success')
                return redirect(url_for('diary.view_entry', entry_id=entry.id))
            
            except Exception as e:
                db.session.rollback()
                logger.error(f"Entry update error: {str(e)}")
                flash('An error occurred while updating your diary entry. Please try again.', 'danger')
        
        elif request.method == 'GET':
            # Pre-fill form with existing entry data
            form.title.data = entry.title
            form.content.data = entry.content
        
        return render_template('create_entry.html', title='Edit Diary Entry', form=form)
    
    except Exception as e:
        logger.error(f"Entry edit error: {str(e)}")
        flash('An error occurred while loading the diary entry. Please try again.', 'danger')
        return redirect(url_for('diary.dashboard'))

@diary.route('/entry/<int:entry_id>/delete', methods=['POST'])
@login_required
def delete_entry(entry_id):
    """Delete a specific diary entry"""
    try:
        entry = DiaryEntry.query.get_or_404(entry_id)
        
        # Check if the entry belongs to the current user
        if entry.user_id != current_user.id:
            logger.warning(f"Unauthorized delete attempt to entry {entry_id} by user {current_user.id}")
            abort(403)
        
        # Delete from database
        db.session.delete(entry)
        db.session.commit()
        logger.info(f"Diary entry deleted: {entry_id} by user {current_user.id}")
        
        flash('Your diary entry has been deleted!', 'success')
        return redirect(url_for('diary.dashboard'))
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Entry delete error: {str(e)}")
        flash('An error occurred while deleting your diary entry. Please try again.', 'danger')
        return redirect(url_for('diary.dashboard'))
