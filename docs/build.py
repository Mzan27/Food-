import zipfile
from xml.sax.saxutils import escape as E
T={
'users':['user_id PK','full_name','email','password_hash','phone','role (customer/admin)','created_at'],
'addresses':['address_id PK','user_id FK->users','street','city','province','is_default'],
'categories':['category_id PK','name','description'],
'products':['product_id PK','category_id FK->categories','name','description','price','stock_qty','image_url','created_at'],
'carts':['cart_id PK','user_id FK->users (UNIQUE)','created_at'],
'cart_items':['cart_item_id PK','cart_id FK->carts','product_id FK->products','quantity'],
'orders':['order_id PK','user_id FK->users','address_id FK->addresses','order_date','status','total_amount'],
'order_items':['order_item_id PK','order_id FK->orders','product_id FK->products','quantity','unit_price'],
'payments':['payment_id PK','order_id FK->orders (UNIQUE)','method','amount','status','paid_at'],
'reviews':['review_id PK','user_id FK->users','product_id FK->products','rating','comment','created_at'],
}
R=[('users','addresses','1:N'),('users','carts','1:1'),('users','orders','1:N'),('addresses','orders','1:N'),('categories','products','1:N'),('carts','cart_items','1:N'),('products','cart_items','1:N'),('orders','order_items','1:N'),('products','order_items','1:N'),('orders','payments','1:1'),('users','reviews','1:N'),('products','reviews','1:N'),('orders / products','N:N via order_items','N:N')]
# ---- ERD SVG
pos={'users':(40,40),'addresses':(40,330),'carts':(40,520),'categories':(900,40),'products':(620,200),'cart_items':(330,520),'orders':(330,40),'order_items':(620,520),'payments':(330,330),'reviews':(900,330)}
W=230;H=lambda n:30+20*len(T[n])
s='<svg xmlns="http://www.w3.org/2000/svg" width="1180" height="720" font-family="Arial" font-size="13"><rect width="100%" height="100%" fill="white"/><text x="20" y="22" font-size="18" font-weight="bold">ERD - Food Shop E-Commerce</text>'
def c(n):x,y=pos[n];return(x+W/2,y+H(n)/2)
L=[('users','addresses','1','N'),('users','carts','1','1'),('users','orders','1','N'),('addresses','orders','1','N'),('categories','products','1','N'),('carts','cart_items','1','N'),('products','cart_items','1','N'),('orders','order_items','1','N'),('products','order_items','1','N'),('orders','payments','1','1'),('users','reviews','1','N'),('products','reviews','1','N')]
for a,b,m,n in L:
  x1,y1=c(a);x2,y2=c(b)
  s+=f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#888" stroke-width="1.5"/>'
  s+=f'<text x="{x1+(x2-x1)*.2}" y="{y1+(y2-y1)*.2-4}" fill="red" font-weight="bold">{m}</text><text x="{x1+(x2-x1)*.8}" y="{y1+(y2-y1)*.8-4}" fill="red" font-weight="bold">{n}</text>'
for n,(x,y) in pos.items():
  s+=f'<rect x="{x}" y="{y}" width="{W}" height="{H(n)}" fill="#fff" stroke="#333" stroke-width="2"/><rect x="{x}" y="{y}" width="{W}" height="26" fill="#e67e22"/><text x="{x+8}" y="{y+18}" fill="white" font-weight="bold">{n}</text>'
  for i,f in enumerate(T[n]):
    col='#c0392b' if 'PK' in f else ('#2471a3' if 'FK' in f else '#000')
    s+=f'<text x="{x+8}" y="{y+46+20*i}" fill="{col}">{E(f)}</text>'
s+='<text x="20" y="700">Red=PK, Blue=FK. 1=one, N=many. N:N orders-products resolved by order_items.</text></svg>'
open('ERD.svg','w').write(s)
# ---- DOCX
P=[]
def h(t,l=1):P.append(f'<w:p><w:pPr><w:pStyle w:val="Heading{l}"/></w:pPr><w:r><w:t>{E(t)}</w:t></w:r></w:p>')
def p(t):P.append(f'<w:p><w:r><w:t xml:space="preserve">{E(t)}</w:t></w:r></w:p>')
def b(l):[p('• '+i) for i in l]
def tb(rows):
  x='<w:tbl><w:tblPr><w:tblBorders>'+''.join(f'<w:{k} w:val="single" w:sz="4"/>' for k in['top','left','bottom','right','insideH','insideV'])+'</w:tblBorders></w:tblPr>'
  for r in rows:x+='<w:tr>'+''.join(f'<w:tc><w:p><w:r><w:t>{E(c)}</w:t></w:r></w:p></w:tc>' for c in r)+'</w:tr>'
  P.append(x+'</w:tbl>');p('')
h('Food Shop - Business and System Planning')
h('1. Business')
tb([['Business / Shop Name','Food Shop'],['Business Idea','Online restaurant/food shop where customers browse the menu, order and pay online, and receive food by delivery or pickup.'],['Products / Services','Breakfast (egg, bacon), salads, fine-dining meat dishes, drinks, desserts; delivery and pickup service.'],['Target Customer','Students, office workers and families in the city who want fast, convenient meals online.'],['E-Commerce Model','B2C (Business to Customer)']])
h('2. System Planning')
h('2.1 System Requirements',2)
p('Functional:');b(['Register/login/logout','Browse products by category, view details, search','Manage cart, checkout, pay','Track order history and status','Admin manages products, categories, orders, users'])
p('Non-functional:');b(['Responsive design (Bootstrap)','Secure passwords (hashed)','Fast page load','Easy to use, Khmer/English friendly'])
p('Technical: HTML, CSS, Bootstrap, JavaScript (front-end); backend and MySQL database (later); Git/GitHub.')
h('2.2 Main Features',2)
b(['Product catalog and categories','Product detail page','Search and filter','Shopping cart','Checkout and payment','Login / Register','Order history and tracking','Reviews and ratings','Admin dashboard'])
h('2.3 User Roles',2)
tb([['Role','Permissions'],['Guest','Browse, search, view products, register'],['Customer','Guest + cart, checkout, orders, reviews, profile'],['Admin','Manage products, categories, orders, customers, reports']])
h('2.4 Business Process',2)
b(['1. Customer browses menu and selects products','2. Adds items to cart','3. Logs in and checks out with address and payment method','4. System creates order and payment record','5. Admin confirms and prepares the order','6. Delivery / pickup','7. Order marked completed; customer may review'])
h('2.5 User Flow',2)
p('Home -> Menu/Category -> Product Detail -> Add to Cart -> Cart -> Login/Register (if not logged in) -> Checkout -> Payment -> Order Confirmation -> My Orders.')
p('Admin: Login -> Dashboard -> Manage Products / Orders -> Update Status.')
h('2.6 Website Sitemap',2)
b(['Home (index.html)','Menu / Products (menu.html) -> Categories -> Product Detail','Search','Cart','Checkout -> Order Confirmation','Login (login.html) / Register (create.html)','My Account -> My Orders, Addresses','Contact / About','Admin -> Dashboard, Products, Categories, Orders, Users'])
h('3. UI Front-End')
p('Front-end pages are uploaded to the GitHub repository (index.html, menu.html, login.html, create.html, and the new pages cart.html, checkout.html, orders.html, product.html).')
tb([['Page','Description'],['Products / Categories','menu.html - category filter and product cards'],['Product Details','product.html - image, price, description, quantity, add to cart'],['Search','Search bar in navbar filters products'],['Cart','cart.html - items, quantity, total'],['Checkout','checkout.html - address, payment, summary'],['Login / Register','login.html, create.html'],['Order','orders.html - order history and status']])
h('4. Database Design')
h('4.1 Tables, PK, FK',2)
for n,f in T.items():
  h(n,3);tb([['Field','Key']]+[[x.split(' ')[0],' '.join(x.split(' ')[1:])] for x in f])
h('4.2 Relationships',2)
tb([['Table A','Table B','Type']]+[list(r) for r in R])
h('4.3 ERD',2)
p('See attached image ERD.svg / ERD.png (submitted with this document).')
body=''.join(P)
d=f'<?xml version="1.0" encoding="UTF-8"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>{body}</w:body></w:document>'
st='<?xml version="1.0" encoding="UTF-8"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'+''.join(f'<w:style w:type="paragraph" w:styleId="Heading{i}"><w:name w:val="heading {i}"/><w:rPr><w:b/><w:sz w:val="{40-6*i}"/></w:rPr></w:style>' for i in(1,2,3))+'</w:styles>'
z=zipfile.ZipFile('Business_System_Planning.docx','w')
z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>')
z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="r1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
z.writestr('word/_rels/document.xml.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="r1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>')
z.writestr('word/document.xml',d);z.writestr('word/styles.xml',st);z.close()
