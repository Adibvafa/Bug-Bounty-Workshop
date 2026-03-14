from django import forms

from .models import Preset


class UploadForm(forms.Form):
    image = forms.ImageField()


class PresetForm(forms.ModelForm):
    dot_spacing = forms.IntegerField(initial=10)
    style = forms.ChoiceField(choices=[("classic", "Classic"), ("diamond", "Diamond"), ("line", "Line")])

    class Meta:
        model = Preset
        fields = ["name", "is_default"]

    def save(self, commit=True):
        preset = super().save(commit=False)
        preset.config = {
            "dot_spacing": self.cleaned_data["dot_spacing"],
            "style": self.cleaned_data["style"],
        }
        if commit:
            preset.save()
        return preset


class PresetImportForm(forms.Form):
    json_data = forms.CharField(widget=forms.Textarea)


class BatchUploadForm(forms.Form):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}))
    make_public = forms.BooleanField(required=False, label="Make all images public")
