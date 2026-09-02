with open("frontend/src/app/page.tsx", "r") as f:
    content = f.read()

old_get_score = """  const getScoreBreakdown = (lead: Lead) => {
    const breakdown = [];
    if (lead.has_website) {
      breakdown.push({ label: 'Website Found', score: '+40', type: 'text-green-600', icon: '✅' });
    } else {
      breakdown.push({ label: 'Missing Website', score: '0', type: 'text-red-500', icon: '❌' });
    }
    
    if (lead.phone) {
      breakdown.push({ label: 'Phone Number Found', score: '+20', type: 'text-green-600', icon: '✅' });
    } else {
      breakdown.push({ label: 'Missing Phone Number', score: '0', type: 'text-red-500', icon: '❌' });
    }
    
    if (lead.whatsapp_link) {
      breakdown.push({ label: 'WhatsApp Link Generated', score: '+20', type: 'text-green-600', icon: '✅' });
    } else {
      breakdown.push({ label: 'Missing WhatsApp', score: '0', type: 'text-red-500', icon: '❌' });
    }
    
    if (lead.rating > 0) {
      breakdown.push({ label: 'Google Rating Found', score: '+20', type: 'text-green-600', icon: '✅' });
    } else {
      breakdown.push({ label: 'Missing Rating', score: '0', type: 'text-red-500', icon: '❌' });
    }
    
    return breakdown;
  };"""

new_get_score = """  const getScoreBreakdown = (lead: Lead) => {
    const breakdown = [];
    if (!lead.has_website) {
      breakdown.push({ label: 'No Website Found (High Priority)', score: '+50', type: 'text-emerald-500', icon: '⭐' });
    } else {
      breakdown.push({ label: 'Has Website (Lower Priority)', score: '0', type: 'text-amber-500', icon: '🌐' });
    }
    
    if (lead.phone) {
      breakdown.push({ label: 'Phone Number Found', score: '+20', type: 'text-emerald-500', icon: '✅' });
    } else {
      breakdown.push({ label: 'Missing Phone Number', score: '0', type: 'text-red-500', icon: '❌' });
    }
    
    if (lead.whatsapp_link) {
      breakdown.push({ label: 'WhatsApp Link Generated', score: '+20', type: 'text-emerald-500', icon: '✅' });
    } else {
      breakdown.push({ label: 'Missing WhatsApp', score: '0', type: 'text-red-500', icon: '❌' });
    }
    
    if (lead.rating > 0) {
      breakdown.push({ label: 'Google Rating Found', score: '+10', type: 'text-emerald-500', icon: '✅' });
    } else {
      breakdown.push({ label: 'Missing Rating', score: '0', type: 'text-red-500', icon: '❌' });
    }
    
    if (lead.email) {
      breakdown.push({ label: 'Email Address Extracted', score: 'Bonus', type: 'text-blue-500', icon: '📧' });
    } else {
      breakdown.push({ label: 'Missing Email', score: '-', type: 'text-muted-foreground', icon: '🚫' });
    }
    
    return breakdown;
  };"""

content = content.replace(old_get_score, new_get_score)

# Fix modal styling
old_modal_header = '<h3 className="text-xl font-bold text-gray-800">Profile Data Completeness</h3>'
new_modal_header = '<h3 className="text-xl font-bold text-foreground">Lead Potential Score</h3>'
content = content.replace(old_modal_header, new_modal_header)

old_modal_box = '<div className="mb-4 bg-gray-50 p-4 rounded-lg border border-gray-100">'
new_modal_box = '<div className="mb-4 bg-muted p-4 rounded-lg border border-border">'
content = content.replace(old_modal_box, new_modal_box)

with open("frontend/src/app/page.tsx", "w") as f:
    f.write(content)
