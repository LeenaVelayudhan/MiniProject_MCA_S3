def manageprofile(request):
    user= user.objects.get(email=request.user.email)  # Assuming email is unique

    if request.method == 'POST':
      
        user.name = request.POST['username']
        user.email = request.POST['email']
        user.password=request.POST['password'] 

       
        user.save()

       
        messages.success(request, 'Profile updated successfully!')
        return redirect('manageprofile')

    return render(request, 'profile.html', {'user': user})
