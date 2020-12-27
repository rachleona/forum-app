# SafeSpace

A simple forum platform practice project with mental health theme, made with flask, sqlite and HTML/CSS + JS. 

<hr />

# Routes

- auth: Login and registration functionalities
- feed: Getting posts in bulk (either logged in user's posts, posts of specified user, or all)
- posts: Creating, editing, fetching one with its comments, liking, and deleting posts
- comments: ^same but for comments
- profile: ^same

<hr />

# Templates
- layout: (layout.html) basic layout of everything, including the navbar, footer and header stuff
          (landing.html) landing page
          (apology.html) template for error display
          
- auth: (login.html) login form
        (register.html) registration
        
- posts: (view.html) display post and comments
         (create.html) create and edit posts
         
- profile: (view.html) display profile
           (edit.html) create and edit profile
           
- feed: (view.html) see posts by a certain user or all
        
 
