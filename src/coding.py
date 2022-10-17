from datetime import datetime

from flask import request, render_template, Flask, session
from werkzeug.utils import redirect

from DBConnection import Db

app=Flask(__name__)
app.secret_key='qwerty'

@app.route('/')
def intro():
    return render_template("homeindex.html")



@app.route('/login')
def login():
    return render_template("loginindex.html")

@app.route('/logi_post', methods=['post'])
def login_post():
    username=request.form['un']
    password=request.form['pwd']
    db=Db()
    qry=" SELECT * FROM `login`WHERE `username`='"+username+"' and`password`='"+password+"'"
    res=db.selectOne(qry)
    if res is None:
        return '''<script>alert("invaild");window.location="/login"</script>'''
    elif res['usertype'] == "admin":
        return '''<script>alert("vaild");window.location="admin"</script>'''
    elif res['usertype'] == "user":
        session['lid']=res['login_id']
        return '''<script>alert("vaild");window.location="user"</script>'''
    else:
        return '''<scrpit>alert("invaild");window.location="/login_index"</scrpit>'''


@app.route('/admin')
def admin_home():
    return render_template("admindash.html")


@app.route('/admin_add_product')
def admin_add_product():
    qry="select * from category"
    db=Db()
    res=db.select(qry)
    return render_template("admin/Addproduct.html",data=res)

@app.route('/admin_add_product_post', methods=['post'])
def admin_add_product_post():
    name=request.form['textfield1']
    price=request.form['textfield2']
    image=request.files['fileField']
    date=datetime.now().strftime("%y%m%d-%H%M%S")
    image.save(r"C:/Users/Hp/PycharmProjects/onlineshopping/src/static/photo/" +date+".jpg")
    path="/static/photo/"+date+".jpg"
    category=request.form['jumpMenu']
    description=request.form['textfield3']
    stock=request.form['stock']

    db = Db()
    # qry1="select * from product where name='"+name+"' "
    # res1=db.select(qry1)
    # if res1 is not None:
    #     return '''<script>alert('Already exist');window.location="/admin_add_product"</script>'''
    # else:
    qry=" INSERT INTO product(`Category_id`,`name`,`price`,`image`,`description`,`stock`) VALUES ('"+category+"','"+name+"','"+price+"','"+path+"','"+description+"','"+stock+"')"
    res=db.insert(qry)
    return '''<script>alert('Successfully added');window.location="/view_admin_product_manage"</script>'''




@app.route('/admin_categories')
def admin_categories():
    return render_template("admin/categories.html")

@app.route('/admin_categories_post', methods=['post'])
def admin_categories_post():
    Category=request.form['textfield']
    Description=request.form['textarea']
    db=Db()
    qry= "INSERT INTO category(`Categoryname`,`Description`) VALUES('"+Category+"','"+Description+"')"
    res=db.insert(qry)
    return '''<script>alert('Successfully added');window.location="/view_admin_category_management"</script>'''



@app.route('/view_admin_category_management')
def view_admin_category_management():
    qry = "select * from category"
    db = Db()
    res = db.select(qry)
    return render_template("admin/categorymanagement.html",data=res)

@app.route('/delete_admin_category_management/<id>')
def delete_admin_category_management(id):
    qry="delete from  category    where Category_id='"+id+"'  "
    db=Db()
    res=db.delete(qry)
    return view_admin_category_management()

@app.route('/edit_admin_category_management/<id>')
def edit_admin_category_management(id):
    qry="select * from category where Category_id='"+id+"'"
    db=Db()
    res=db.selectOne(qry)
    return render_template("admin/editcategories.html",data=res)

@app.route('/edit_admin_category_management_post',methods=['post'])
def edit_admin_category_management_post():
    Category = request.form['textfield']
    Description = request.form['textarea']
    id=request.form['cat']
    qry="update category set Categoryname='"+Category+"',Description='"+Description+"' where Category_id='"+id+"' "
    db=Db()
    res=db.update(qry)
    return view_admin_category_management()




@app.route('/view_admin_product_manage')
def view_admin_product_manage():
    qry = "SELECT * FROM `product` INNER JOIN `category` ON `category`.`Category_id`=`product`.`Category_id`"
    db = Db()
    res = db.select(qry)
    qry1 = "select * from category"
    res1 = db.select(qry1)
    return render_template("admin/productmanagement.html",data=res,data1=res1)



@app.route('/search_admin_product_post',methods=['post'])
def search_admin_product_post():
    select=request.form['jumpMenu']
    qry = "SELECT * FROM `product` INNER JOIN `category` ON `category`.`Category_id`=`product`.`Category_id` where `category`.`Category_id`='"+select+"'"
    print(qry)
    db = Db()
    res = db.select(qry)
    qry1 = "select * from category"
    res1 = db.select(qry1)
    return render_template("admin/productmanagement.html", data=res, data1=res1)


@app.route('/delete_view_admin_product_manage/<id>')
def delete_view_admin_product_manage(id):
    qry = "delete from  product    where Product_id='" + id + "'  "
    db = Db()
    res = db.delete(qry)
    return view_admin_product_manage()



@app.route('/admin_edit_product/<id>')
def admin_edit_product(id):
    db=Db()
    qry="SELECT `product`.* ,`category`.`Category_id`,`category`.`Categoryname` FROM `product` INNER JOIN `category` ON `category`.`Category_id`=`product`.`Category_id` AND product.Product_id='"+ id +"'  "
    res=db.selectOne(qry)
    qry1="select * from category"
    res1=db.select(qry1)
    return render_template("admin/editproduct.html",data=res,data1=res1)

@app.route('/admin_edit_product_post',methods=['post'])
def admin_edit_product_post():
    name = request.form['textfield1']
    price = request.form['textfield2']
    image = request.files['fileField']
    date = datetime.now().strftime("%y%m%d-%H%M%S")
    image.save(r"C:/Users/Hp/PycharmProjects/onlineshopping/src/static/photo/" + date + ".jpg")
    path = "/static/photo/" + date + ".jpg"
    category = request.form['jumpMenu']
    description = request.form['textfield3']
    stock=request.form['stock']
    id = request.form['cat']
    qry=" update product set name='"+name+"',price='"+price+"',image='"+path+"',description='"+description+"',stock='"+stock+"', Category_id='"+category+"' where Product_id='"+id+"'  "
    db=Db()
    res=db.update(qry)
    return view_admin_product_manage()



@app.route('/view_admin_feedback')
def view_admin_feedback():
    qry="SELECT `product`.*,`registration`.*,`feedback`.* FROM `feedback` JOIN `product` ON `feedback`.`Product_id`=`product`.`Product_id` JOIN `registration` ON `registration`.`login_id`=`feedback`.`user_id`"
    db=Db()
    res=db.select(qry)
    return render_template("admin/feedback.html",data=res)

@app.route('/search_admin_feedback_post',methods=['post'])
def search_admin_feedback_post():
    From=request.form['textfield']
    To=request.form['textfield2']

    qry = "SELECT `product`.*,`registration`.*,`feedback`.* FROM `feedback` JOIN `product` ON `feedback`.`Product_id`=`product`.`Product_id` JOIN `registration` ON `registration`.`login_id`=`feedback`.`user_id` where `feedback`.Date between '"+From+"' and '"+To+"'"
    db = Db()
    res = db.select(qry)

    return render_template("admin/feedback.html",data=res)




@app.route('/view_admin_orders')
def view_admin_orders():
    qry= " SELECT `order`.*,`registration`.* FROM `order` JOIN `registration` ON `registration`.`login_id`=`order`.`user_id` "
    db=Db()
    res=db.select(qry)
    return render_template("admin/vieworders.html",data=res)

@app.route('/view_admin_orders_post',methods=['post'])
def view_admin_orders_post():
    return "ok"



@app.route('/view_admin_order_more/<id>')
def view_admin_order_more(id):
    qry=" SELECT * FROM `product` INNER JOIN  orderdetails ON `product`.`Product_id`=`orderdetails`.`Product_id` INNER JOIN `category` ON `product`.`Category_id`=`category`.`Category_id` INNER JOIN `order` ON `order`.`order_id`=`orderdetails`.`order_id`  "
    db=Db()
    res=db.select(qry)
    tot = 0
    for i in res:
        tot += float(i['price']) * float(i['Quantity'])
    return render_template("admin/ordermore.html", data=res, ij=tot)

    # return render_template("admin/ordermore.html",data=res)

@app.route('/view_admin_order_more_post',methods=['post'])
def view_admin_order_more_post():
    return "ok"





@app.route('/view_admin_custom_order')
def view_admin_custom_order():
    qry="SELECT `customorder`.*,`registration`.* FROM `customorder` JOIN `registration` ON `registration`.`login_id`=`customorder`.`user_id`"
    db=Db()
    res=db.select(qry)
    return render_template("admin/viewcustomorder.html",data=res)

@app.route('/view_admin_custom_order_post',methods=['post'])
def view_admin_custom_order_post():
    return "ok"

@app.route('/approve_custorder/<id>')
def approve_custorder(id):
    qry="UPDATE customorder set Status='Approved' where cust_id='"+id+"' "
    db=Db()
    res=db.update(qry)
    return redirect('/view_approved_custorder')

@app.route('/view_approved_custorder')
def view_approved_custorder():
    qry = "SELECT `customorder`.*,`registration`.* FROM `customorder` JOIN `registration` ON `registration`.`login_id`=`customorder`.`user_id` where Status='Approved'"
    db = Db()
    res = db.select(qry)
    return render_template("admin/viewapprovedcustomorder.html",data=res)



@app.route('/reject_custorder/<id>')
def reject_custorder(id):
    qry = "UPDATE customorder set Status='Rejected' where cust_id='" + id + "' "
    db = Db()
    res = db.update(qry)
    return redirect('/view_reject_customorder')

@app.route('/view_reject_customorder')
def view_reject_customorder():
    qry = "SELECT `customorder`.*,`registration`.* FROM `customorder` JOIN `registration` ON `registration`.`login_id`=`customorder`.`user_id` where Status='Rejected'"
    db = Db()
    res = db.select(qry)
    return render_template("admin/viewrejectedcustomorder.html", data=res)


@app.route('/view_admin_custom_order_more/<id>')
def view_admin_custom_order_more(id):
    qry="SELECT `customorder`.*,`registration`.* FROM `customorder` JOIN `registration` ON `registration`.`login_id`=`customorder`.`user_id` where cust_id='"+id+"'"
    db=Db()
    res=db.select(qry)
    return render_template("admin/customordermore.html",data=res)

@app.route('/view_admin_custom_order_more_post',methods=['post'])
def view_admin_custom_order_more_post():
    return "ok"




@app.route('/view_admin_payment')
def view_admin_payment():
    qry="SELECT * FROM `payment` INNER JOIN `order` ON `order`.`order_id`=`payment`.`order_id` INNER JOIN `registration` ON `registration`.`login_id`=`order`.`user_id`"
    db=Db()
    res=db.select(qry)
    return render_template("admin/Payment.html",data=res)

@app.route('/view_admin_payment_post',methods=['post'])
def view_admin_payment_post():
    return "ok"




@app.route('/view_admin_refund')
def view_admin_refund():
    qry=" SELECT `registration`.`username`,`product`.`name`,`order`.`Amount`,`return`.* FROM `return` INNER JOIN `order` ON `order`.`order_id`=`return`.`order_id` INNER JOIN`registration` ON `registration`.`login_id`=`order`.`user_id` INNER JOIN `product` ON `product`.`Product_id`=`return`.`Product_id` where `return`.Status='Pending' "
    db=Db()
    res=db.select(qry)
    return render_template("admin/Refund.html",data=res)

@app.route('/view_admin_refund_post',methods=['post'])
def view_admin_refund_post():
    return "ok"

@app.route('/approved_refund_product/<id>')
def approved_refund_product(id):
    qry="update `return` set Status='Pending' where return_id='"+id+"'"
    db=Db()
    res=db.update(qry)
    qry1="update `order"
    return redirect('/view_approved_refund')

@app.route('/view_approved_refund')
def view_approved_refund():
    qry=" SELECT `registration`.`username`,`product`.`name`,`order`.`Amount`,`return`.* FROM `return` INNER JOIN `order` ON `order`.`order_id`=`return`.`order_id` INNER JOIN`registration` ON `registration`.`login_id`=`order`.`user_id` INNER JOIN `product` ON `product`.`Product_id`=`return`.`Product_id` where `return`.Status='Approved' "
    db=Db()
    res=db.select(qry)
    return render_template("admin/Refundapproved.html",data=res)

@app.route('/approved_refund/<id>')
def approved_refund(id):
    db=Db()
    qry=" update `return` set Status='Approved' where return_id='"+id+"'"
    res=db.update(qry)
    return redirect('/view_approved_refund')

@app.route('/rejected_refund/<id>')
def rejected_refund(id):
    db=Db()
    qry=" Update `return` set Status='Rejected' where return_id='"+id+"'"
    res=db.update(qry)
    return redirect('/view_rejected_refund')

@app.route('/view_rejected_refund')
def view_rejected_refund():
    db=Db()
    qry=" SELECT `registration`.`username`,`product`.`name`,`order`.`Amount`,`return`.* FROM `return` INNER JOIN `order` ON `order`.`order_id`=`return`.`order_id` INNER JOIN`registration` ON `registration`.`login_id`=`order`.`user_id` INNER JOIN `product` ON `product`.`Product_id`=`return`.`Product_id` where `return`.Status='Rejected' "
    res=db.select(qry)
    return render_template("admin/Refundrejected.html",data=res)










@app.route('/user')
def user_home():
    return render_template("userindex.html")

@app.route('/user_registration')
def user_registration():
    return render_template("regindex.html")

@app.route('/user_registration_post',methods=['post'])
def user_registration_post():
    name=request.form['textfield']
    email=request.form['textfield2']
    place=request.form['textfield4']
    post=request.form['textfield5']
    pin=request.form['textfield6']
    city=request.form['textfield7']
    phone=request.form['textfield8']
    password = request.form['textfield9']
    confirm = request.form['textfield3']

    db=Db()

    qry2="select * from `login` where `username`='"+email+"' "
    res2=db.selectOne(qry2)
    if res2 is None:

        qry=" INSERT INTO `login` (`username`,`password`,`usertype`) VALUES('"+email+"','"+password+"','user')"
        res=db.insert(qry)

        qry1=" INSERT INTO `registration`(`login_id`,`username`,`place`,`post`,`pin`,`city`,`emailid`,`phoneno`) VALUES ( '"+str(res)+"','"+name+"','"+place+"','"+post+"','"+pin+"','"+city+"','"+email+"','"+phone+"') "
        res1=db.insert(qry1)

        return '''<script>alert('Registration success');window.location="/login"</script>'''
    else:
        return '''<script>alert('User already exist.');history.back()</script>'''


# @app.route('forget_password')
# def forget_password():
#     render_template("")


@app.route('/user_profile')
def user_profile():
    qry=" select * from registration where login_id='"+str(session['lid'])+"'"
    db=Db()
    res=db.selectOne(qry)
    return render_template("user/userviewprofile.html",data=res)

@app.route('/user_profile_post',methods=['post'])
def user_profile_post():
    name = request.form['textfield']
    email = request.form['textfield6']
    place = request.form['textfield2']
    post = request.form['textfield3']
    pin = request.form['textfield4']
    city = request.form['textfield5']
    phone = request.form['textfield7']
    db=Db()
    qry="update registration set username='"+name+"',place='"+place+"',post='"+post+"',pin='"+pin+"',city='"+city+"',emailid='"+email+"',phoneno='"+phone+"' where login_id='"+str(session['lid'])+"' "
    res=db.update(qry)
    return redirect('/user_profile')



@app.route('/user_updateprofile')
def user_updateprofile():
    qry = " select * from registration where login_id='" + str(session['lid']) + "'"
    db = Db()
    res = db.selectOne(qry)
    return render_template("user/userprofile.html",data=res)



@app.route('/user_viewproduct')
def user_viewproduct():
    qry = "SELECT * FROM `product` INNER JOIN `category` ON `category`.`Category_id`=`product`.`Category_id` and product.stock!=0"
    db = Db()
    res = db.select(qry)
    qry1 = "select * from category"
    res1 = db.select(qry1)
    return render_template("user/userviewproduct.html", data=res, data1=res1)


@app.route('/user_viewproduct_post',methods=['post'])
def user_viewproduct_post():
    cat=request.form['jumpMenu']
    qry = "SELECT * FROM `product` INNER JOIN `category` ON `category`.`Category_id`=`product`.`Category_id` where category.Category_id like '%"+cat+"%' "
    db = Db()
    res = db.select(qry)
    qry1="select * from category"
    res1=db.select(qry1)
    return render_template("user/userviewproduct.html",data=res,data1=res1)


@app.route('/user_addcart/<id>')
def user_addcart(id):
    db=Db()
    qry="SELECT * FROM `product` INNER JOIN `category` ON `category`.`Category_id`=`product`.`Category_id` where Product_id='"+id+"'"
    res=db.selectOne(qry)

    return render_template("user/usercart.html",data=res)

@app.route('/user_addcart_post',methods=['post'])
def user_addcart_post():
    name=request.form['name']
    price=request.form['price']
    quantity=request.form['textfield']
    db=Db()
    qry="INSERT INTO `cart` (`Product_id`,`Quantity`,`user_id`) VALUES ('"+name+"','"+quantity+"','"+str(session['lid'])+"')"
    res=db.insert(qry)
    return redirect('/user_viewproduct')

@app.route('/user_viewcart')
def user_viewcart():
    db=Db()
    qry="SELECT * FROM `cart` INNER JOIN `product` ON `cart`.`Product_id`=`product`.`Product_id` WHERE user_id='"+str(session['lid'])+"' "
    res=db.select(qry)
    return render_template("user/userviewcart.html",data=res)


@app.route('/user_removecart/<id>')
def user_removecart(id):
    qry = "delete from  cart where cart_id='" + id + "'  "
    db = Db()
    res = db.delete(qry)
    return user_viewcart()


@app.route('/user_order')
def user_order():
    qry="SELECT * FROM `order` WHERE user_id='"+str(session["lid"])+"'"
    db=Db()
    res=db.select(qry)
    if len(res)>0:
        p="yes"
    else:
        p="no"
    return render_template("user/userorders.html",data=res,p=p)

@app.route('/user_order_post',methods=['post'])
def user_order_post():
    acc=request.form['textfield']
    ifsc=request.form['textfield2']
    # pin=request.form['textfield2']
    # password=request.form['textfield3']
    address=request.form["address"]
    print(address)
    if address =="no":
        place=request.form['textfield4']
        post=request.form['textfield5']
        pincode=request.form['textfield6']
        city=request.form['textfield7']
        district=request.form['textfield8']
        # payment=request.form['textfield9']
        house=request.form['textfield3']
        email=request.form['textfield']
        phoneno=request.form['textfield9']
    else:
        qry = "SELECT * FROM `order` WHERE order_id='" + address + "'"
        db = Db()
        res = db.selectOne(qry)
        place=res["Place"]
        post = res['Post']
        pincode = res['Pin']
        city = res['City']
        district = res['District']
        # payment=request.form['textfield9']
        house = res['House']
        email = res['Email']
        phoneno = res['Phoneno']
    db=Db()
    r="select * from product "
    q=db.select(r)
    qry = "SELECT * FROM `cart` INNER JOIN `product` ON `cart`.`Product_id`=`product`.`Product_id` WHERE user_id='" + str(
            session['lid']) + "' "
    res = db.select(qry)
    qry1=" INSERT INTO `order` (`user_id`,`House`,`Place`,`Post`,`Pin`,`City`,`District`,`DeliveryDate`,`Phoneno`,`Email`,`Status`,`Amount`) VALUES ('"+str(session['lid'])+"','"+house+"','"+place+"' ,'"+post+"','"+pincode+"','"+city+"','"+district+"' ,curdate(),'"+phoneno+"','"+email+"','ordered','0')"
    res1=db.insert(qry1)
    print(qry1)
    for i in res:
        qry2="insert into orderdetails(order_id,Product_id,Quantity)values('"+str(res1)+"','"+str(i['Product_id'])+"','"+str(i['Quantity'])+"')"
        res2=db.insert(qry2)
        qqry4="UPDATE `product` SET `stock`=`stock`-'"+str(i['Quantity'])+"' WHERE `Product_id`='"+str(i['Product_id'])+"'"
        db.update(qqry4)
        qry3="SELECT SUM(price*Quantity)as sum FROM `orderdetails`  INNER JOIN `order` ON `order`.`order_id`=`orderdetails`.`order_id` INNER JOIN `product` ON `product`.`Product_id`=`orderdetails`.`Product_id`   WHERE `order`.order_id='"+str(res1)+"'"
        res3=db.selectOne(qry3)
        qry4="update `order` set Amount='"+str(res3['sum'])+"' where order_id='"+str(res1)+"'"
        res4=db.update(qry4)
        qry5="delete from cart where Product_id='"+str(i['Product_id'])+"'"
        res5=db.delete(qry5)
        return redirect('/user')



@app.route('/user_customorders')
def user_customorders():
    qry = "SELECT * FROM `order` WHERE user_id='" + str(session["lid"]) + "'"
    db = Db()
    res = db.select(qry)
    print(res)

    if len(res) > 0:
        p = "yes"
    else:
        p = "no"
    return render_template("user/usercustomorder.html",data=res,p=p)


@app.route('/user_customorders_post',methods=['post'])
def user_customorders_post():
    image=request.files['fileField']
    date=datetime.now().strftime("%y%m%d-%H%M%S")
    image.save(r"C:/Users/Hp/PycharmProjects/onlineshopping/src/static/materialphoto/" + date + ".jpg")
    path = "/static/materialphoto/" + date + ".jpg"
    color=request.form['textfield2']
    material=request.form['textfield']
    quantity=request.form['textfield3']
    db=Db()
    qry="INSERT INTO `customorder`(`user_id`,`image`,`color`,`material`,`quantity`) VALUES ('"+str(session['lid'])+"','"+str(path)+"','"+color+"','"+material+"','"+quantity+"')"
    res=db.insert(qry)
    qry = "SELECT * FROM `order` WHERE user_id='" + str(session["lid"]) + "'"
    db = Db()
    res = db.select(qry)
    print(res)

    if len(res) > 0:
        p = "yes"
    else:
        p = "no"
    return render_template("user/userorders.html",data=res,p=p)







@app.route('/user_vieworder')
def user_vieworder():
    db=Db()
    qry=" SELECT * FROM `order` WHERE user_id='"+str(session['lid'])+"'"
    res=db.select(qry)

    return render_template("user/uservieworder.html",data=res)


@app.route('/user_viewordermore/<id>')
def user_viewordermore(id):
    db=Db()
    qry="SELECT * FROM `product` INNER JOIN  orderdetails ON `product`.`Product_id`=`orderdetails`.`Product_id` INNER JOIN `category` ON `product`.`Category_id`=`category`.`Category_id` "
    res=db.select(qry)
    tot=0
    for i in res:
        tot+=float(i['price'])*float(i['Quantity'])
    return render_template("user/userordermore.html",data=res,ij=tot)




@app.route('/user_feedback')
def user_feedback():
    return render_template("user/useraddfeedback.html")

@app.route('/user_cancelorder/<id>')
def user_cancelorder(id):
    return render_template("user/usercancelorder.html",data=id)



@app.route('/user_cancelorder_post',methods=['post'])
def user_cancelorder_post():
    db=Db()
    id=request.form['id']
    qry1="UPDATE `order` SET `Status`='cancelled' WHERE `order_id`='"+str(id)+"'"
    res1=db.update(qry1)
    print(res1)
    for i in res1:
        qry2="UPDATE `product` SET `stock`='"+i['quantity']+"' WHERE`Product_id`='"+id+"' "
        res2=db.update(qry2)
        return redirect("user/uservieworder.html")
    qry3="insert into return values('','')"

    # qry3="UPDATE `return` SET `Status`='"++"' WHERE `order_id`='"+id+"' "
    # res3=db.update(qry3)
    #
    # qry4="UPDATE `payment` SET `Status`='"++"' WHERE `order_id`='"+id+"' "
    # res4=db.update(qry4)
    #
    # return render_template("user/usercancelorder.html")



if __name__=='__main__':
    app.run(debug=True)
