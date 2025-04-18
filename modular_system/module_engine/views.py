from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Module
import subprocess
from django.http import JsonResponse


@login_required(login_url="/login/")
def module_manager(request):
    if not request.user.is_superuser:
        return redirect("/products/")

    try:
        modules = Module.load_modules()

        if request.method == "POST":
            action = request.POST.get("action")
            module_name = request.POST.get("module_name")

            try:
                module = Module.objects.get(name=module_name)

                if action == "install":
                    module.installed = True
                    module.active = True
                    module.save()
                    messages.success(
                        request, f"Module {module_name} installed successfully!"
                    )

                elif action == "uninstall":
                    module.installed = False
                    module.active = False
                    module.save()
                    messages.success(
                        request, f"Module {module_name} uninstalled successfully!"
                    )
                    return redirect("module_manager")

                elif action == "upgrade":
                    module.upgrade_module()
                    messages.success(
                        request, f"Module {module_name} upgraded successfully!"
                    )

            except Module.DoesNotExist:
                messages.error(request, "Module not found!")

            return redirect("module_manager")

        return render(
            request, "module_engine/module_manager.html", {"modules": modules}
        )

    except Exception as e:
        messages.error(request, f"Error loading modules: {str(e)}")
        return render(request, "module_engine/module_manager.html", {"modules": []})

@login_required(login_url="/login/")
def module_upgrade_form(request, module_name):
    try:
        module = Module.objects.get(name=module_name)
        app_label = module.name.lower() 
        model_name = "Product" 

        from django.apps import apps
        Product = apps.get_model(app_label=app_label, model_name=model_name)

        fields = Product._meta.get_fields()
        if request.method == 'POST':
            # belum selesai permintaannya apakah merubah table?
            return redirect("module_manager")

        return render(request, "module_engine/module_upgrade_form.html", {
            "module": module,
            "fields": fields
        })

    except Exception as e:
        messages.error(request, f"Upgrade error: {str(e)}")
        return redirect("module_manager")
