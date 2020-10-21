from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect

converter = Flask(__name__)
converter.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///converter.db'
converter.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
data_base = SQLAlchemy(converter)


class Currency(data_base.Model):
    __tablename__ = 'currency_rates'
    currency_id = data_base.Column(data_base.Integer, primary_key=True)
    currency_name = data_base.Column(data_base.String(5), nullable=False)
    currency_rate = data_base.Column(data_base.Integer, nullable=False)

    # def __repr__(self):
    #     return '<chart %r>' % self.currency_id


data_base.create_all()


@converter.route('/', methods=['POST', 'GET'])
def index():
    try:
        if request.method == 'POST':
            field_content = request.form['number']
            currency_name = request.form['currency']
            new_var = float(field_content)
            currency = Currency.query.filter(Currency.currency_name == currency_name).one_or_none()
            currency_rate = currency.currency_rate
            result = new_var * currency_rate
            formated_result = format(result, ',.5f')
            chart = Currency.query.order_by(Currency.currency_id).all()
            return render_template('index.html', text=formated_result, chart=chart)
        else:
            chart = Currency.query.order_by(Currency.currency_id).all()
            return render_template('index.html', chart=chart)
    except ValueError:
        return 'Моля, въведете сума'


@converter.route('/admin', methods=['POST', 'GET'])
def store_info():
    if request.method == 'POST':
        currency_content = request.form['currencytype']
        currency_rate = request.form['currencyrate']
        # formated_currency_rate = float(currency_rate)
        new_task = Currency(currency_name=currency_content, currency_rate=currency_rate)
        data_base.session.add(new_task)
        data_base.session.commit()
        chart = Currency.query.order_by(Currency.currency_id).all()
        return render_template('admin.html', chart=chart)
        #     return redirect('admin.html')
        # except:
        #     return 'Възникна грешка при обработката на заявката'
    else:
        chart = Currency.query.order_by(Currency.currency_id).all()
        return render_template('admin.html', chart=chart)


@converter.route('/update/<int:currency_id>', methods=['GET', 'POST'])
def update(currency_id):
    chart = Currency.query.get_or_404(currency_id)
    if request.method == 'POST':
        chart.currency_name = request.form['content']   # поправка chart.currency ---> chart.currency_name
        chart.currency_rate = request.form['number']
        data_base.session.commit()
        return redirect('/admin')
        # except:
        #     return 'Възникна грешка при обработката на заявката'
    else:
        return render_template('update.html', chart=chart)


if __name__ == "__main__":
    converter.run(debug=True)
