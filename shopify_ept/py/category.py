
# from odoo import api, fields, models, tools
from odoo import tools
from odoo import models,fields,api

class product_public_category(models.Model):
    _name = "product.public.category"
    _description = "Public Category"
    _order = "sequence, name"

    _sql_constraints = [
        ('_check_recursion', 'unique(parent_id)', 'Error ! You cannot create recursive categories.')
    ]

    def name_get(self):
        res = []
        for cat in self.browse(self._ids):
            names = [cat.name]
            pcat = cat.parent_id
            while pcat:
                names.append(pcat.name)
                pcat = pcat.parent_id
            res.append((cat.id, ' / '.join(reversed(names))))
        return res

    def _name_get_fnc(self, prop, unknow_none):
        res = self.name_get()
        return dict(res)

    def _get_image(self, name, args):
        result = dict.fromkeys(self._ids, False)
        for obj in self.browse(self._ids):
            result[obj.id] = tools.image_get_resized_images(obj.image)
        return result

    def _set_image(self, name, value, args):
        return self.write([id], {'image': tools.image_resize_image_big(value)})


    name = fields.Char('Name', required=True, translate=True)
    complete_name = fields.Char(compute='_name_get_fnc', String='Name')
    parent_id = fields.Many2one('product.public.category','Parent Category', select=True)
    child_id = fields.One2many('product.public.category', 'parent_id', String='Children Categories')
    sequence = fields.Integer('Sequence', help="Gives the sequence order when displaying a list of product categories.")

        # NOTE: there is no 'default image', because by default we don't show thumbnails for categories. However if we have a thumbnail
        # for at least one category, then we display a default image on the other, so that the buttons have consistent styling.
        # In this case, the default image is set by the js code.
        # NOTE2: image: all image fields are base64 encoded and PIL-supported
    image = fields.Binary("Image",
            help="This field holds the image used as image for the category, limited to 1024x1024px.")
    image_medium = fields.Binary(compute='_get_image', inverse='_set_image',
            String="Medium-sized image", multi="_get_image", store=True,
            # store={
            #     'product.public.category': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            # },
            help="Medium-sized image of the category. It is automatically "\
                 "resized as a 128x128px image, with aspect ratio preserved. "\
                 "Use this field in form views or some kanban views.")
    image_small = fields.Binary(compute='_get_image', inverse='_set_image',
            String="Smal-sized image", multi="_get_image", store=True,
            # store={
            #     'product.public.category': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
            # },
            help="Small-sized image of the category. It is automatically "\
                 "resized as a 64x64px image, with aspect ratio preserved. "\
                 "Use this field anywhere a small image is required.")



