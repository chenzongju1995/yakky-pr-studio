import os, json
from datetime import date, datetime
from flask import Flask, render_template, request, jsonify
from models import Base, Sample, Loan, Contact, Tracking, init_db, get_session

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'yakky-pr-studio-secret')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_URL = os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR}/yakky.db')
engine = init_db(DB_URL)

def db():
    return get_session(engine)

# Auto-seed demo data on first launch if DB is empty
if os.environ.get('SEED_DEMO_DATA') == '1':
    s = db()
    try:
        if s.query(Sample).count() == 0:
            from init_db import seed_demo_data
            seed_demo_data(s)
    finally:
        s.close()

# ==================== 页面 ====================

@app.route('/')
def index():
    return render_template('index.html')

# ==================== 样衣 API ====================

@app.route('/api/samples')
def api_samples():
    s = db()
    try:
        items = []
        for r in s.query(Sample).order_by(Sample.created_at.desc()).all():
            items.append({
                'id': r.code, 'name': r.name, 'cat': r.category,
                'size': r.size, 'color': r.color, 'status': r.status,
                'borrower': r.borrower, 'due': r.due, '_id': r.id
            })
        return jsonify(items)
    finally:
        s.close()

@app.route('/api/samples', methods=['POST'])
def api_sample_add():
    s = db()
    try:
        data = request.get_json()
        sample = Sample(
            code=data['id'], name=data['name'], category=data.get('cat', ''),
            size=data.get('size', ''), color=data.get('color', ''),
            status=data.get('status', 'in'), borrower=data.get('borrower', ''),
            due=data.get('due', '')
        )
        s.add(sample)
        s.commit()
        return jsonify({'ok': True, '_id': sample.id})
    except Exception as e:
        s.rollback()
        return jsonify({'ok': False, 'error': str(e)}), 400
    finally:
        s.close()

@app.route('/api/samples/<int:sid>', methods=['PUT'])
def api_sample_edit(sid):
    s = db()
    try:
        sample = s.query(Sample).get(sid)
        if not sample:
            return jsonify({'ok': False, 'error': '不存在'}), 404
        data = request.get_json()
        for k in ['code', 'name', 'category', 'size', 'color', 'status', 'borrower', 'due']:
            key_map = {'code': 'id', 'category': 'cat'}
            dk = key_map.get(k, k)
            if dk in data:
                setattr(sample, k, data[dk])
        s.commit()
        return jsonify({'ok': True})
    except Exception as e:
        s.rollback()
        return jsonify({'ok': False, 'error': str(e)}), 400
    finally:
        s.close()

@app.route('/api/samples/<int:sid>', methods=['DELETE'])
def api_sample_delete(sid):
    s = db()
    try:
        sample = s.query(Sample).get(sid)
        if sample:
            s.delete(sample)
            s.commit()
        return jsonify({'ok': True})
    finally:
        s.close()

# ==================== 借用 API ====================

@app.route('/api/loans')
def api_loans():
    s = db()
    try:
        items = []
        for r in s.query(Loan).order_by(Loan.created_at.desc()).all():
            items.append({
                'id': r.loan_id, 'item': r.item_name, 'borrower': r.borrower_name,
                'type': r.loan_type, 'lend': r.lend_date, 'due': r.due_date,
                'track': r.tracking_no, 'status': r.status, '_id': r.id
            })
        return jsonify(items)
    finally:
        s.close()

@app.route('/api/loans', methods=['POST'])
def api_loan_add():
    s = db()
    try:
        data = request.get_json()
        loan = Loan(
            loan_id=data['id'], item_name=data.get('item', ''),
            borrower_name=data.get('borrower', ''), loan_type=data.get('type', '博主'),
            lend_date=data.get('lend', ''), due_date=data.get('due', ''),
            tracking_no=data.get('track', ''), status=data.get('status', 'active')
        )
        s.add(loan)
        s.commit()
        return jsonify({'ok': True, '_id': loan.id})
    except Exception as e:
        s.rollback()
        return jsonify({'ok': False, 'error': str(e)}), 400
    finally:
        s.close()

@app.route('/api/loans/<int:lid>', methods=['PUT'])
def api_loan_edit(lid):
    s = db()
    try:
        loan = s.query(Loan).get(lid)
        if not loan:
            return jsonify({'ok': False, 'error': '不存在'}), 404
        data = request.get_json()
        for k in ['loan_id', 'item_name', 'borrower_name', 'loan_type', 'lend_date', 'due_date', 'tracking_no', 'status']:
            dk = {'loan_id': 'id', 'item_name': 'item', 'borrower_name': 'borrower', 'loan_type': 'type',
                  'lend_date': 'lend', 'due_date': 'due', 'tracking_no': 'track'}.get(k, k)
            if dk in data:
                setattr(loan, k, data[dk])
        s.commit()
        return jsonify({'ok': True})
    except Exception as e:
        s.rollback()
        return jsonify({'ok': False, 'error': str(e)}), 400
    finally:
        s.close()

@app.route('/api/loans/<int:lid>', methods=['DELETE'])
def api_loan_delete(lid):
    s = db()
    try:
        loan = s.query(Loan).get(lid)
        if loan:
            s.delete(loan)
            s.commit()
        return jsonify({'ok': True})
    finally:
        s.close()

# ==================== 联系人 API ====================

@app.route('/api/contacts')
def api_contacts():
    s = db()
    try:
        items = []
        for r in s.query(Contact).order_by(Contact.name).all():
            items.append({
                'name': r.name, 'handle': r.handle, 'type': r.contact_type,
                'platform': r.platform, 'fans': r.fans, 'loans': r.loan_count,
                'rating': r.rating, '_id': r.id
            })
        return jsonify(items)
    finally:
        s.close()

@app.route('/api/contacts', methods=['POST'])
def api_contact_add():
    s = db()
    try:
        data = request.get_json()
        c = Contact(
            name=data['name'], handle=data.get('handle', ''),
            contact_type=data.get('type', '博主'), platform=data.get('platform', ''),
            fans=data.get('fans', ''), loan_count=data.get('loans', 0),
            rating=data.get('rating', 'A')
        )
        s.add(c)
        s.commit()
        return jsonify({'ok': True, '_id': c.id})
    except Exception as e:
        s.rollback()
        return jsonify({'ok': False, 'error': str(e)}), 400
    finally:
        s.close()

@app.route('/api/contacts/<int:cid>', methods=['PUT'])
def api_contact_edit(cid):
    s = db()
    try:
        c = s.query(Contact).get(cid)
        if not c:
            return jsonify({'ok': False, 'error': '不存在'}), 404
        data = request.get_json()
        for k in ['name', 'handle', 'contact_type', 'platform', 'fans', 'loan_count', 'rating']:
            dk = {'contact_type': 'type', 'loan_count': 'loans'}.get(k, k)
            if dk in data:
                setattr(c, k, data[dk])
        s.commit()
        return jsonify({'ok': True})
    except Exception as e:
        s.rollback()
        return jsonify({'ok': False, 'error': str(e)}), 400
    finally:
        s.close()

@app.route('/api/contacts/<int:cid>', methods=['DELETE'])
def api_contact_delete(cid):
    s = db()
    try:
        c = s.query(Contact).get(cid)
        if c:
            s.delete(c)
            s.commit()
        return jsonify({'ok': True})
    finally:
        s.close()

# ==================== 快递 API ====================

@app.route('/api/trackings')
def api_trackings():
    s = db()
    try:
        items = []
        for r in s.query(Tracking).order_by(Tracking.id.desc()).all():
            items.append({
                'no': r.tracking_no, 'carrier': r.carrier, 'from': r.from_party,
                'to': r.to_party, 'item': r.item_name, 'status': r.status, '_id': r.id
            })
        return jsonify(items)
    finally:
        s.close()

@app.route('/api/trackings', methods=['POST'])
def api_tracking_add():
    s = db()
    try:
        data = request.get_json()
        t = Tracking(
            tracking_no=data['no'], carrier=data.get('carrier', ''),
            from_party=data.get('from', ''), to_party=data.get('to', ''),
            item_name=data.get('item', ''), status=data.get('status', 'transit')
        )
        s.add(t)
        s.commit()
        return jsonify({'ok': True, '_id': t.id})
    except Exception as e:
        s.rollback()
        return jsonify({'ok': False, 'error': str(e)}), 400
    finally:
        s.close()

@app.route('/api/trackings/<int:tid>', methods=['PUT'])
def api_tracking_edit(tid):
    s = db()
    try:
        t = s.query(Tracking).get(tid)
        if not t:
            return jsonify({'ok': False, 'error': '不存在'}), 404
        data = request.get_json()
        for k in ['tracking_no', 'carrier', 'from_party', 'to_party', 'item_name', 'status']:
            dk = {'tracking_no': 'no', 'from_party': 'from', 'to_party': 'to', 'item_name': 'item'}.get(k, k)
            if dk in data:
                setattr(t, k, data[dk])
        s.commit()
        return jsonify({'ok': True})
    except Exception as e:
        s.rollback()
        return jsonify({'ok': False, 'error': str(e)}), 400
    finally:
        s.close()

@app.route('/api/trackings/<int:tid>', methods=['DELETE'])
def api_tracking_delete(tid):
    s = db()
    try:
        t = s.query(Tracking).get(tid)
        if t:
            s.delete(t)
            s.commit()
        return jsonify({'ok': True})
    finally:
        s.close()

# ==================== 统计 API ====================

@app.route('/api/stats')
def api_stats():
    s = db()
    try:
        contacts = s.query(Contact).order_by(Contact.loan_count.desc()).all()
        stats_list = []
        for c in contacts:
            stats_list.append({
                'name': c.name, 'type': c.contact_type, 'count': c.loan_count,
                'avg': 9, 'overdue': 0, 'rating': c.rating
            })
        if not stats_list:
            stats_list = [
                {'name': '暂无数据', 'type': '-', 'count': 0, 'avg': 0, 'overdue': 0, 'rating': '-'}
            ]
        return jsonify({
            'avg_cycle': '—',
            'utilization': 0,
            'overdue_rate': '—',
            'month_flow': 0,
            'stats_list': stats_list,
            'chart_data': [0, 0, 0, 0, 0, 0],
        })
    finally:
        s.close()

# ==================== 快递查询 ====================

@app.route('/api/express/<tracking_no>')
def api_express(tracking_no):
    return jsonify({
        'success': True,
        'traces': [
            {'ftime': '2026-05-25 10:30', 'context': '快件已到达【北京朝阳分部】'},
            {'ftime': '2026-05-25 08:15', 'context': '快件离开【北京转运中心】'},
            {'ftime': '2026-05-24 22:00', 'context': '快件已从【上海转运中心】发出'},
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug, port=port, host='0.0.0.0')
