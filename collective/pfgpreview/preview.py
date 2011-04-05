from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.PloneFormGen import implementedOrProvidedBy
from Products.Archetypes.interfaces.field import IField
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class PreviewPFGView(BrowserView):
    """ Browser view that can update and render a PFG form in some other context
    """
    render = ViewPageTemplateFile("fg_confirmpage.pt")

    def title(self):
        return self.context.title
    
    def preview(self):
        errors = self.context.fgvalidate(REQUEST=self.request, errors=None, data=1, metadata=0, skip_action_adapters=True)
        if errors:
            return self.request.traverse('/'.join(self.context.getPhysicalPath()))()
            #return self.request.traverse(self.context.absolute_url_path())()
        if self.context.getRawAfterValidationOverride():
            # evaluate the override.
            # In case we end up traversing to a template,
            # we need to make sure we don't clobber
            # the expression context.
            self.context.getAfterValidationOverride()
            self.context.cleanExpressionContext(request=self.request)
            
        return self.render()

    def displayInputs(self):
        """ Returns sequence of dicts {'label':fieldlabel, 'value':input}
        """
        # get a list of all candidate fields
        request = self.request
        context = self.context
        myFields = []
        tp = getattr(context, context.thanksPage, None)
        if not tp:
            return []
        for obj in context._getFieldObjects():
            if (not implementedOrProvidedBy(IField, obj) or obj.isLabel()):
                # if field list hasn't been specified explicitly, exclude server side fields
                if tp.showAll and obj.getServerSide():
                    continue 
                myFields.append(obj)

        # Now, determine which fields we show
        if tp.showAll:
            sFields = myFields
        else:
            sFields = []
            # acquire field list from parent
            res = []
            for id in tp.showFields:
                # inefficient if we get many fields
                for f in myFields:
                    if f.getId() == id:
                        sFields.append(f)
                        break

        # Now, build the results list
        res = []
        for obj in sFields:
            value = obj.htmlValue(request)
            if tp.includeEmpties or (value and (value != 'No Input')):
                res.append( {
                    'label' : obj.fgField.widget.label,
                    'value' : value,
                    } )

        return res
