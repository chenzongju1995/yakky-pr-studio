"""Initialize database with demo data for YAKKY PR Studio."""
from models import Base, Sample, Loan, Contact, Tracking, init_db, get_session

def seed_demo_data(session):
    """Seed the given session with demo data."""
    samples = [
        Sample(code='PR-001', name='白色衬衫连衣裙', category='连衣裙', size='S', color='白', status='in', borrower='', due=''),
        Sample(code='PR-002', name='黑色皮革夹克', category='外套', size='M', color='黑', status='lent', borrower='林小美 @linxiaomei', due='2026-05-28'),
        Sample(code='PR-003', name='藏青色西装套装', category='套装', size='L', color='藏青', status='transit', borrower='张雅琴摄影工作室', due='2026-06-05'),
        Sample(code='PR-004', name='米色针织毛衣', category='上装', size='M', color='米', status='in', borrower='', due=''),
        Sample(code='PR-005', name='酒红色缎面礼服', category='礼服', size='S', color='酒红', status='overdue', borrower='王美颜 @wangmeiyan', due='2026-05-18'),
        Sample(code='PR-006', name='卡其色风衣', category='外套', size='L', color='卡其', status='lent', borrower='时尚芭莎', due='2026-06-10'),
        Sample(code='PR-007', name='牛仔阔腿裤', category='下装', size='M', color='蓝', status='in', borrower='', due=''),
        Sample(code='PR-008', name='印花真丝衬衫', category='上装', size='S', color='多色', status='lent', borrower='陈晓红 @chenxiaohong', due='2026-05-30'),
    ]
    for x in samples:
        session.add(x)
    session.commit()

    contacts = [
        Contact(name='林小美', handle='@linxiaomei', contact_type='博主', platform='小红书', fans='120万', loan_count=8, rating='A'),
        Contact(name='王美颜', handle='@wangmeiyan', contact_type='博主', platform='微博', fans='85万', loan_count=12, rating='B'),
        Contact(name='张雅琴', handle='张雅琴工作室', contact_type='摄影师', platform='商业合作', fans='—', loan_count=6, rating='A'),
        Contact(name='陈晓红', handle='@chenxiaohong', contact_type='博主', platform='抖音', fans='230万', loan_count=15, rating='A'),
        Contact(name='时尚芭莎', handle='媒体合作', contact_type='媒体', platform='杂志', fans='—', loan_count=3, rating='A'),
        Contact(name='刘艺彤', handle='@liuyitong', contact_type='博主', platform='小红书', fans='60万', loan_count=5, rating='B'),
    ]
    for x in contacts:
        session.add(x)
    session.commit()

    loans = [
        Loan(loan_id='LN-047', item_name='黑色皮革夹克 PR-002', borrower_name='林小美', loan_type='博主', lend_date='2026-05-18', due_date='2026-05-28', tracking_no='SF1234567890', status='active'),
        Loan(loan_id='LN-046', item_name='酒红色缎面礼服 PR-005', borrower_name='王美颜', loan_type='博主', lend_date='2026-05-10', due_date='2026-05-18', tracking_no='YT9876543210', status='overdue'),
        Loan(loan_id='LN-045', item_name='藏青色西装套装 PR-003', borrower_name='张雅琴工作室', loan_type='摄影师', lend_date='2026-05-20', due_date='2026-06-05', tracking_no='JD5566778899', status='active'),
        Loan(loan_id='LN-044', item_name='卡其色风衣 PR-006', borrower_name='时尚芭莎', loan_type='媒体', lend_date='2026-05-15', due_date='2026-06-10', tracking_no='ZT1122334455', status='active'),
        Loan(loan_id='LN-043', item_name='印花真丝衬衫 PR-008', borrower_name='陈晓红', loan_type='博主', lend_date='2026-05-19', due_date='2026-05-30', tracking_no='SF9988776655', status='active'),
        Loan(loan_id='LN-042', item_name='白色衬衫连衣裙 PR-001', borrower_name='刘艺彤', loan_type='博主', lend_date='2026-04-10', due_date='2026-04-25', tracking_no='SF1111222233', status='returned'),
    ]
    for x in loans:
        session.add(x)
    session.commit()

    trackings = [
        Tracking(tracking_no='SF1234567890', carrier='顺丰', from_party='PR仓库', to_party='林小美', item_name='黑色皮革夹克', status='transit'),
        Tracking(tracking_no='YT9876543210', carrier='圆通', from_party='王美颜', to_party='PR仓库', item_name='酒红缎面礼服', status='abnormal'),
        Tracking(tracking_no='JD5566778899', carrier='京东', from_party='PR仓库', to_party='张雅琴', item_name='藏青西装套装', status='transit'),
        Tracking(tracking_no='ZT1122334455', carrier='中通', from_party='PR仓库', to_party='时尚芭莎', item_name='卡其色风衣', status='delivered'),
        Tracking(tracking_no='SF9988776655', carrier='顺丰', from_party='PR仓库', to_party='陈晓红', item_name='印花真丝衬衫', status='transit'),
    ]
    for x in trackings:
        session.add(x)
    session.commit()
    print('Seeded 8 samples, 6 contacts, 6 loans, 5 trackings.')

if __name__ == '__main__':
    engine = init_db('sqlite:///yakky.db')
    s = get_session(engine)
    for t in [Tracking, Loan, Sample, Contact]:
        s.query(t).delete()
    s.commit()
    seed_demo_data(s)
    s.close()
