from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from olmsapp.models import CustomUser,Category,Author,Book,Student,Issuedbookdetails
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
import decimal
from django.db.models import Q
User = get_user_model()


@login_required(login_url='/')
def ADD_CATEGORY(request):
    if request.method == "POST":
        catname = request.POST.get('catname')
        status = request.POST.get('status')
        cat =Category(
            catname=catname,
            status=status,
        )
        cat.save()
        messages.success(request,'Category has been added succeesfully!!!')
        return redirect("add_category")
    
    return render(request,'admin/add-category.html')

@login_required(login_url='/')
def MANAGE_CATEGORY(request):
    
    cat_list = Category.objects.all()
    paginator = Paginator(cat_list, 10)  # Show 10 categories per page

    page_number = request.GET.get('page')
    try:
        categories = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        categories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        categories = paginator.page(paginator.num_pages)

    context = {'categories': categories,
    }
    return render(request, 'admin/manage_category.html', context)

@login_required(login_url='/')
def DELETE_CATEGORY(request,id):
    cat = Category.objects.get(id=id)
    cat.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    
    return redirect('manage_category')


login_required(login_url='/')
def UPDATE_CATEGORY(request,id):
    cat = Category.objects.get(id=id)
    
    context = {
         'cat':cat,
        
    }

    return render(request,'admin/update_category.html',context)

login_required(login_url='/')

def UPDATE_CATEGORY_DETAILS(request):
        if request.method == 'POST':
          cat_id = request.POST.get('cat_id')
          catname = request.POST.get('catname')
          status = request.POST.get('status')
          category = Category.objects.get(id=cat_id) 
          category.catname = catname
          category.status = status
          category.save()   
          messages.success(request,"Your category detail has been updated successfully")
          return redirect('manage_category')
        return render(request, 'admin/update_category.html')


@login_required(login_url='/')
def ADD_AUTHOR(request):
    if request.method == "POST":
        authorname = request.POST.get('authorname')
        
        authorinfo =Author(
            authorname=authorname,
            
        )
        authorinfo.save()
        messages.success(request,'Author info has been added succeesfully!!!')
        return redirect("add_author")
    
    return render(request,'admin/add-author.html')

@login_required(login_url='/')
def MANAGE_AUTHOR(request):
    
    auth_list = Author.objects.all()
    paginator = Paginator(auth_list, 10)  # Show 10 authors per page

    page_number = request.GET.get('page')
    try:
        authors = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        authors = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        authors = paginator.page(paginator.num_pages)

    context = {'authors': authors,
    }
    return render(request, 'admin/manage_author.html', context)

@login_required(login_url='/')
def DELETE_AUTHOR(request,id):
    auth = Author.objects.get(id=id)
    auth.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    
    return redirect('manage_author')

login_required(login_url='/')
def UPDATE_AUTHOR(request,id):
    auth = Author.objects.get(id=id)
    
    context = {
         'auth':auth,
        
    }

    return render(request,'admin/update_author.html',context)

login_required(login_url='/')

def UPDATE_AUTHOR_DETAILS(request):
        if request.method == 'POST':
          auth_id = request.POST.get('auth_id')
          authorname = request.POST.get('authorname')
          authors = Author.objects.get(id=auth_id) 
          authors.authorname = authorname
          authors.save()   
          messages.success(request,"Your author detail has been updated successfully")
          return redirect('manage_author')
        return render(request, 'admin/update_author.html')

@login_required(login_url='/')
def ADD_BOOKS(request):
    categories = Category.objects.all()
    authors = Author.objects.all()

    if request.method == "POST":
        bookname = request.POST.get('bookname')
        catid = request.POST.get('catid')
        authid = request.POST.get('authid')
        isbnnum = request.POST.get('isbnnum')
        price = request.POST.get('price')
        bookimage = request.FILES.get('bookimage')

        try:
            category = Category.objects.get(id=catid)
            author = Author.objects.get(id=authid)
        except (Category.DoesNotExist, Author.DoesNotExist):
            messages.error(request, 'Invalid category or author ID')
            return redirect('add_books')

        bookinfo = Book(
            bookname=bookname,
            catid=category,
            authid=author,
            isbnnum=isbnnum,
            price=price,
            bookimage=bookimage,
            isIssued='0'
        )

        bookinfo.save()
        messages.success(request, 'Book info has been added successfully!')
        return redirect('add_books')

    context = {
        'categories': categories,
        'authors': authors,
    }
    return render(request, 'admin/add-books.html', context)


@login_required(login_url='/')
def MANAGE_BOOKS(request):
    
    book_list = Book.objects.all()
    paginator = Paginator(book_list, 10)  # Show 10 books per page

    page_number = request.GET.get('page')
    try:
        books = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        books = paginator.page(paginator.num_pages)

    context = {'books': books,
    }
    return render(request, 'admin/manage_books.html', context)

@login_required(login_url='/')
def DELETE_BOOKS(request,id):
    books = Book.objects.get(id=id)
    books.delete()
    messages.success(request,'Record Delete Succeesfully!!!')
    return redirect('manage_books')


login_required(login_url='/')
def UPDATE_BOOKS(request,id):
    books = Book.objects.get(id=id)
    context = {
         'books':books,
        
    }
    return render(request,'admin/update_books.html',context)

login_required(login_url='/')

def UPDATE_BOOKS_DETAILS(request):
        if request.method == 'POST':
          book_id = request.POST.get('book_id')
          bookname = request.POST.get('bookname')
          authid = request.POST.get('authid')
          cat_id = request.POST.get('catid')
          isbnnum = request.POST.get('isbnnum')
          price = request.POST.get('price')
          bookimage = request.FILES.get('bookimage')
          try:
            books = get_object_or_404(Book,id=book_id)
            category = get_object_or_404(Category, id=cat_id)
            author = get_object_or_404(Author, id=authid)
            books.bookname = bookname
            books.authid = author
            books.catid = category
            books.isbnnum = isbnnum
            books.price = price
            if bookimage:
                books.bookimage = bookimage

            books.save()   
            messages.success(request,"Your author detail has been updated successfully")
            return redirect('manage_books')

          except (Author.DoesNotExist, Category.DoesNotExist, Book.DoesNotExist):
            messages.error(request, "Invalid ID provided for subcategory, category, or news post")
            return redirect('update_books')
        return render(request, 'admin/update_books.html')

login_required(login_url='/')
def ISSUE_BOOK(request):
    students = Student.objects.all()
    books = Book.objects.all()
    context = {'books': books,
    'students':students
    }
    return render(request,'admin/issue_book.html',context)


@login_required(login_url='/')
def ISSUE_BOOK(request):
    if request.method == 'POST':
        book_id = request.POST.get('bookid')
        stud_id = request.POST.get('stuid')
        try:
            # Fetch the Book instance
            book = Book.objects.get(id=book_id)
            student = Student.objects.get(id=stud_id)
            
            # Create the issued book record
            issued_book = Issuedbookdetails.objects.create(
                book_id=book,  # Pass the Book instance
                stud_id=student,
            )
            issued_book.save()

            # Update the isIssued field in the Book model
            book.isIssued = True  # Assuming isIssued is a BooleanField
            book.save()

            messages.success(request, 'Book issued successfully!')
            return redirect('issue_book')  # Replace with your success URL
        except Exception as e:
            messages.error(request, f'Error issuing book: {e}')
            return redirect('issue_book')  # Redirect back to the issue book page
    else:
        students = Student.objects.all()
        # Filter books that have not been issued
        books = Book.objects.filter(Q(isIssued='0') | Q(isIssued='Return'))
        context = {
            'books': books,
            'students': students
        }
        return render(request, 'admin/issue_book.html', context)


@login_required(login_url='/')
def MANAGE_ISSUEDBOOKS(request):
    
    issuebook_list = Issuedbookdetails.objects.all()
    paginator = Paginator(issuebook_list, 10)  # Show 10 issued_books per page

    page_number = request.GET.get('page')
    try:
        issued_books = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        issued_books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        issued_books = paginator.page(paginator.num_pages)

    context = {'issued_books': issued_books,
    }
    return render(request, 'admin/manage_issuedbook.html', context)

login_required(login_url='/')
def UPDATE_IBSTATUS(request,id):
    iss_books = Issuedbookdetails.objects.get(id=id)
    context = {
         'iss_books':iss_books,
                   
    }
    return render(request,'admin/update_issue_book_details.html',context)

login_required(login_url='/')
def UPDATE_IBSTATUS_DETAILS(request):
        if request.method == 'POST':
          book_id = request.POST.get('bookid')
          issbkid = request.POST.get('issbk_id')
          fine = request.POST.get('fine')
         
          try:
            books = get_object_or_404(Book,id=book_id)
            issbks = get_object_or_404(Issuedbookdetails, id=issbkid)
            
            books.isIssued = "Return"
            issbks.return_status = "Return"
            issbks.fine = fine
            

            books.save()   
            issbks.save() 
            messages.success(request,"Issue book detail has been updated successfully")
            return redirect('manage_issued_books')

          except (Book.DoesNotExist, Issuedbookdetails.DoesNotExist):
            messages.error(request, "Invalid ID provided for book or issue book")
            return redirect('update_ib_status')
        return render(request, 'admin/manage_issuedbook.html')

@login_required(login_url='/')
def MANAGE_REGUSERS(request):
    
    student_list = Student.objects.all()
    paginator = Paginator(student_list, 10)  # Show 10 student list per page

    page_number = request.GET.get('page')
    try:
        student_list = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        student_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        student_list = paginator.page(paginator.num_pages)

    context = {'student_list': student_list,
    }
    return render(request, 'admin/manage_regusers.html', context)

@login_required(login_url='/')
def DELETE_REGUSERS(request, id):
    try:
        student = get_object_or_404(Student, id=id)
        custom_user = student.admin  # Access the related CustomUser
        student.delete()  # This will also delete the associated CustomUser because of the on_delete=models.CASCADE
        custom_user.delete()
        messages.success(request, 'Record deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting record: {e}')
    return redirect('manage_regusers')


@login_required(login_url='/')
def STUDENT_LIB_HISTORY(request,id):
    
    issuebook_list = Issuedbookdetails.objects.filter(stud_id=id)
    paginator = Paginator(issuebook_list, 10)  # Show 10 issued_books per page

    page_number = request.GET.get('page')
    try:
        issued_books = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        issued_books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        issued_books = paginator.page(paginator.num_pages)

    context = {'issued_books': issued_books,
    }
    return render(request, 'admin/student_lib_history.html', context)

@login_required(login_url='/')
def SEARCHBOOK(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            
            searchbook = Book.objects.filter(bookname__icontains=query) | Book.objects.filter(authid__authorname__icontains=query) | Book.objects.filter(isbnnum__icontains=query)
            messages.info(request, "Search against " + query)
            return render(request, 'admin/search-book.html', {'searchbook': searchbook, 'query': query})
        else:
            return render(request, 'admin/search-book.html', {})

@login_required(login_url='/')
def SEARCHREGUSERS(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            
            searchreguser = Student.objects.filter(mobilenumber__icontains=query) | Student.objects.filter(admin__first_name__icontains=query) | Student.objects.filter(admin__last_name__icontains=query) | Student.objects.filter(studentid__icontains=query)
            messages.info(request, "Search against " + query)
            return render(request, 'admin/search-regusers.html', {'searchreguser': searchreguser, 'query': query})
        else:
            return render(request, 'admin/search-regusers.html', {})