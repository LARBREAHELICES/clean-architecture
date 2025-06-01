import { useState } from "react"
import {
  format,
  startOfMonth,
  endOfMonth,
  startOfWeek,
  endOfWeek,
  addDays,
  isSameMonth,
  isSameDay,
  isAfter,
  isBefore,
  min,
  max,
} from "date-fns"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"

type EventType = {
  id: number
  title: string
  prof: string
  eleves: number
  ecole: string
  matiere: string
  commentaire: string
  startDate: Date
  endDate: Date
}

export default function CalendarPage() {
  const [currentMonth, setCurrentMonth] = useState(new Date())
  const [selectedEvent, setSelectedEvent] = useState<EventType | null>(null)
  const [selectionStart, setSelectionStart] = useState<Date | null>(null)
  const [selectionEnd, setSelectionEnd] = useState<Date | null>(null)
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [events, setEvents] = useState<EventType[]>([])
  const [formData, setFormData] = useState({
    title: "",
    prof: "",
    eleves: "",
    ecole: "",
    matiere: "",
    commentaire: "",
  })

  function onDateClick(day: Date) {
    // Si pas de début ou sélection terminée, démarrer une nouvelle sélection
    if (!selectionStart || (selectionStart && selectionEnd)) {
      setSelectionStart(day)
      setSelectionEnd(null)
      setIsDialogOpen(false)
    } else {
      // Sinon finir la sélection
      if (isBefore(day, selectionStart)) {
        setSelectionEnd(selectionStart)
        setSelectionStart(day)
      } else {
        setSelectionEnd(day)
      }
      setIsDialogOpen(true)
    }
  }

  // Fonction pour savoir si une date est dans la sélection
  function isDateSelected(date: Date) {
    if (!selectionStart) return false
    if (!selectionEnd) return isSameDay(date, selectionStart)

    // Calculer bornes min et max pour ne pas dépendre de l'ordre sélectionné
    const start = min([selectionStart, selectionEnd])
    const end = max([selectionStart, selectionEnd])

    return date >= start && date <= end
  }

  // Savoir si c'est la première date sélectionnée (pour arrondir à gauche)
  function isSelectionStart(date: Date) {
    if (!selectionStart || !selectionEnd) return false
    const start = min([selectionStart, selectionEnd])
    return isSameDay(date, start)
  }

  // Savoir si c'est la dernière date sélectionnée (pour arrondir à droite)
  function isSelectionEnd(date: Date) {
    if (!selectionStart || !selectionEnd) return false
    const end = max([selectionStart, selectionEnd])
    return isSameDay(date, end)
  }

  const prevMonth = () => setCurrentMonth(addDays(currentMonth, -30))
  const nextMonth = () => setCurrentMonth(addDays(currentMonth, 30))

  const startDate = startOfWeek(startOfMonth(currentMonth), { weekStartsOn: 1 })
  const endDate = endOfWeek(endOfMonth(currentMonth), { weekStartsOn: 1 })

  const renderCells = () => {
    const days = [];
    let day = startDate;
    let keyId = 0;
  
    while (day <= endDate) {
      const dayCopy = new Date(day)
      const isSelected = isDateSelected(dayCopy)
      const isCurrentMonth = isSameMonth(dayCopy, currentMonth)
  
      let baseClasses =
        "flex flex-col justify-between h-24 border border-gray-700 rounded-md p-1 cursor-pointer select-none transition-colors"
  
      if (isSelected) {
        if (isSelectionStart(dayCopy)) {
          baseClasses += " rounded-l-lg bg-violet-800 text-white"
        } else if (isSelectionEnd(dayCopy)) {
          baseClasses += " rounded-r-lg bg-violet-800 text-white"
        } else {
          baseClasses += " bg-violet-700 text-white"
        }
      } else if (isCurrentMonth) {
        baseClasses += " bg-gray-800 text-gray-200 hover:bg-violet-700"
      } else {
        baseClasses += " bg-gray-700 text-gray-500"
      }
  
      days.push(
        <div
          key={keyId++}
          className={baseClasses}
          onClick={() => onDateClick(dayCopy)}
          title={format(dayCopy, "PPP")}
        >
          <div className="text-right text-xs font-semibold">{format(dayCopy, "d")}</div>
          <div className="flex-1 overflow-hidden text-ellipsis">
            {events
              .filter(
                (ev) =>
                  isSameDay(dayCopy, ev.startDate) ||
                  (ev.startDate < dayCopy && ev.endDate >= dayCopy)
              )
              .map((ev) => (
                <div
                  key={ev.id}
                  className="bg-violet-700 text-white rounded px-1 text-[10px] truncate mb-0.5"
                  title={`${ev.title} (${format(ev.startDate, "dd/MM")} - ${format(ev.endDate, "dd/MM")})`}
                >
                  {ev.title}
                  <br />
                  {ev.prof && <span className="text-xs">{ev.prof}</span>}
                  <br />
                  {ev.eleves > 0 && (
                    <span className="text-xs ml-1">{ev.eleves}</span>
                  )}
                  <br />
                  {ev.ecole && <span className="text-xs ml-1">{ev.ecole}</span>}
                  <br />
                </div>
              ))}
          </div>
        </div>
      );
  
      day = addDays(day, 1)
    }
  
    return days
  }  

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) {
    const { id, value } = e.target
    setFormData((prev) => ({ ...prev, [id]: value }))
  }

  function saveEvent() {
    if (!selectionStart || !selectionEnd) return
    if (!formData.title.trim()) {
      alert("Le titre est obligatoire")
      return
    }
    if (selectedEvent) {
      // Modification
      setEvents((prev) =>
        prev.map((ev) =>
          ev.id === selectedEvent.id
            ? {
                ...ev,
                title: formData.title,
                prof: formData.prof,
                eleves: Number(formData.eleves) || 0,
                ecole: formData.ecole,
                matiere: formData.matiere,
                commentaire: formData.commentaire,
                startDate: selectionStart,
                endDate: selectionEnd,
              }
            : ev
        )
      )
    } else {
      // Création
      const newEvent: EventType = {
        id: events.length + 1,
        title: formData.title,
        prof: formData.prof,
        eleves: Number(formData.eleves) || 0,
        ecole: formData.ecole,
        matiere: formData.matiere,
        commentaire: formData.commentaire,
        startDate: selectionStart,
        endDate: selectionEnd,
      }
      setEvents((prev) => [...prev, newEvent])
    }
    closeDialog()
  }

  function deleteEvent() {
    if (!selectedEvent) return
    if (window.confirm("Voulez-vous vraiment supprimer cet événement ?")) {
      setEvents((prev) => prev.filter((ev) => ev.id !== selectedEvent.id))
      closeDialog()
    }
  }

  function onEventClick(ev: EventType) {
    setSelectedEvent(ev)
    setIsDialogOpen(true)
    setSelectionStart(ev.startDate)
    setSelectionEnd(ev.endDate)
    setFormData({
      title: ev.title,
      prof: ev.prof,
      eleves: ev.eleves.toString(),
      ecole: ev.ecole,
      matiere: ev.matiere,
      commentaire: ev.commentaire,
    })
    setCurrentMonth(ev.startDate)
    setCurrentMonth(ev.startDate)
  }

  function closeDialog() {
    setIsDialogOpen(false)
    setSelectedEvent(null)
    setSelectionStart(null)
    setSelectionEnd(null)
    setFormData({
      title: "",
      prof: "",
      eleves: "",
      ecole: "",
      matiere: "",
      commentaire: "",
    })
  }

  return (
    <div className="max-w-7xl mx-auto flex gap-4 p-4 bg-gray-900 text-gray-200 min-h-screen">
      <div className="flex-1">
        <h1 className="text-2xl font-bold mb-4">Calendrier mensuel</h1>
        <div className="flex justify-between items-center mb-4">
          <Button variant="outline" onClick={prevMonth}>
            Mois précédent
          </Button>
          <h2 className="text-xl font-semibold">{format(currentMonth, "MMMM yyyy")}</h2>
          <Button variant="outline" onClick={nextMonth}>
            Mois suivant
          </Button>
        </div>

        <div className="grid grid-cols-7 gap-1">
          {["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"].map((d) => (
            <div key={d} className="text-center font-semibold text-gray-400">
              {d}
            </div>
          ))}
        </div>

        <div className="mt-2 grid grid-cols-7 gap-1">{renderCells()}</div>

        {isDialogOpen && (
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogContent className="max-w-md">
              <DialogHeader>
                <DialogTitle>{selectedEvent ? "Modifier un événement" : "Créer un événement"}</DialogTitle>
              </DialogHeader>
              <div className="grid gap-4">
                {/* mêmes inputs que tu avais */}
                <div>
                  <Label htmlFor="title">Titre</Label>
                  <Input
                    id="title"
                    value={formData.title}
                    onChange={handleChange}
                    placeholder="Titre de l'événement"
                    className="bg-gray-700 text-gray-200 border-gray-600"
                  />
                </div>
                <div>
                  <Label htmlFor="prof">Professeur</Label>
                  <Input
                    id="prof"
                    value={formData.prof}
                    onChange={handleChange}
                    placeholder="Nom du professeur"
                    className="bg-gray-700 text-gray-200 border-gray-600"
                  />
                </div>
                <div>
                  <Label htmlFor="eleves">Nombre d'élèves</Label>
                  <Input
                    id="eleves"
                    type="number"
                    min={0}
                    value={formData.eleves}
                    onChange={handleChange}
                    placeholder="Nombre d'élèves"
                    className="bg-gray-700 text-gray-200 border-gray-600"
                  />
                </div>
                <div>
                  <Label htmlFor="ecole">École</Label>
                  <Input
                    id="ecole"
                    value={formData.ecole}
                    onChange={handleChange}
                    placeholder="École"
                    className="bg-gray-700 text-gray-200 border-gray-600"
                  />
                </div>
                <div>
                  <Label htmlFor="matiere">Matière</Label>
                  <Input
                    id="matiere"
                    value={formData.matiere}
                    onChange={handleChange}
                    placeholder="Matière"
                    className="bg-gray-700 text-gray-200 border-gray-600"
                  />
                </div>
                <div>
                  <Label htmlFor="commentaire">Commentaire</Label>
                  <Textarea
                    id="commentaire"
                    value={formData.commentaire}
                    onChange={handleChange}
                    placeholder="Notes complémentaires"
                    rows={3}
                    className="bg-gray-700 text-gray-200 border-gray-600"
                  />
                </div>
              </div>
              <div className="mt-4 flex justify-between items-center gap-2">
                {selectedEvent && (
                  <Button variant="destructive" onClick={deleteEvent}>
                    Supprimer
                  </Button>
                )}
                <div className="ml-auto flex gap-2">
                  <Button variant="outline" onClick={closeDialog}>
                    Annuler
                  </Button>
                  <Button onClick={saveEvent}>
                    {selectedEvent ? "Enregistrer" : "Créer"}
                  </Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        )}
      </div>

      <aside className="w-72 border-l border-gray-700 p-3 overflow-y-auto max-h-[80vh] bg-gray-800 text-gray-200 rounded">
        <h2 className="text-lg font-semibold mb-3">Événements</h2>
        {events.length === 0 && <p className="text-gray-400">Aucun événement</p>}
        <ul>
          {events.map((ev) => (
            <li
              key={ev.id}
              onClick={() => onEventClick(ev)}
              className="cursor-pointer p-2 rounded hover:bg-violet-700 truncate"
              title={`${ev.title} (${format(ev.startDate, "PPP")} - ${format(ev.endDate, "PPP")})`}
            >
              <strong className="block truncate">{ev.title}</strong>
              <small className="text-xs text-gray-400 block">
                {format(ev.startDate, "dd/MM/yyyy")} - {format(ev.endDate, "dd/MM/yyyy")}
              </small>
            </li>
          ))}
        </ul>
      </aside>
    </div>
  )
}
