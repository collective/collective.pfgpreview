from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.PloneFormGen import implementedOrProvidedBy
from Products.Archetypes.interfaces.field import IField

class PreviewPFGView(BrowserView):
    """ Browser view that can update and render a PFG form in some other context
    """
    def displayInputs(self):
        """ Returns sequence of dicts {'label':fieldlabel, 'value':input}
        """
        # get a list of all candidate fields
        request = self.request
        context = self.context
        myFields = []
        #print self, getattr(self, '_getFieldObjects', 'Not')
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
